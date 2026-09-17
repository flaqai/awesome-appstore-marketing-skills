"""Behavioral checks for collection, provenance and incomplete responses."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

SCRIPT = Path(__file__).resolve().parents[1] / "skills/app-store-opportunity-research/scripts/collect_app_store.py"
spec = importlib.util.spec_from_file_location("collector", SCRIPT)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def response(data):
    return io.BytesIO(json.dumps(data).encode())


class CollectorTests(unittest.TestCase):
    def test_same_id_merges_queries_but_not_similar_names(self):
        apps = {}
        item = {"trackId": 1, "trackName": "AI Music", "wrapperType": "software", "price": 0}
        c.add_apps(apps, {"results": [item]}, "us", "url-a", "ai music")
        c.add_apps(apps, {"results": [item, dict(item, trackId=2)]}, "us", "url-b", "song")
        self.assertEqual(len(apps), 2)
        self.assertEqual([m["term"] for m in apps["1"]["query_matches"]], ["ai music", "song"])
        self.assertEqual(apps["2"]["query_matches"][0]["response_position"], 2)
        self.assertIsNone(apps["1"]["userRatingCount"])
        self.assertEqual(apps["1"]["price"], 0)

    def test_review_metadata_ignored_and_single_entry_supported(self):
        item = {"id": {"label": "123"}, "im:rating": {"label": "2"}, "content": {"label": "Failed export"}}
        a = c.parse_reviews({"feed": {"entry": [{"id": {"label": "metadata"}}, item]}}, "9", "us", "url")
        b = c.parse_reviews({"feed": {"entry": item}}, "9", "us", "url")
        self.assertEqual(a, b)
        self.assertEqual(a[0]["rating"], 2)
        self.assertEqual(a[0]["app_id"], "9")

    @patch.object(c.time, "sleep")
    def test_rate_limit_retries_then_preserves_raw_response(self, sleep):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); (p / "raw").mkdir()
            col = c.Collector(p)
            err = HTTPError("https://example.org", 429, "rate limit", {}, None)
            with patch.object(c, "urlopen", side_effect=[err, response({"results": []})]) as request:
                self.assertEqual(col.fetch("https://example.org", "search"), {"results": []})
            self.assertEqual(request.call_count, 2)
            self.assertEqual(col.requests[0]["attempts"], 2)
            self.assertTrue((p / col.requests[0]["raw_file"]).is_file())

    @patch.object(c.time, "sleep")
    def test_partial_failure_still_saves_other_queries(self, sleep):
        with tempfile.TemporaryDirectory() as tmp:
            err = HTTPError("https://example.org", 403, "forbidden", {}, None)
            item = {"trackId": 7, "wrapperType": "software", "primaryGenreName": "Music"}
            with patch.object(c, "urlopen", side_effect=[err, response({"results": [item]})]):
                code = c.main(["--keyword", "music", "--term", "song", "--output", tmp])
            self.assertEqual(code, 2)
            manifest = json.loads((Path(tmp) / "manifest.json").read_text())
            self.assertFalse(manifest["complete"])
            self.assertEqual(manifest["unique_app_count"], 1)
            self.assertEqual(manifest["failed_request_count"], 1)

    def test_invalid_json_shape_is_failure_not_empty_market(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); (p / "raw").mkdir()
            col = c.Collector(p)
            with patch.object(c, "urlopen", return_value=response({"error": "unavailable"})):
                self.assertIsNone(col.fetch("https://example.org", "search"))
            self.assertEqual(col.requests[0]["status"], "error")

    @patch.object(c.time, "sleep")
    def test_lookup_and_duplicate_review_pages(self, sleep):
        item = {"trackId": 9, "wrapperType": "software", "trackName": "Found by ID"}
        review = {"id": {"label": "456"}, "im:rating": {"label": "5"}}
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(c, "urlopen", side_effect=[response({"results": []}), response({"results": [item]}),
                    response({"feed": {"entry": [review]}}), response({"feed": {"entry": [review]}})]):
                self.assertEqual(c.main(["--keyword", "unknown", "--app-id", "9", "--review-app-id", "9",
                                        "--review-pages", "2", "--output", tmp]), 0)
            self.assertEqual(len(json.loads((Path(tmp) / "reviews.json").read_text())), 1)
            apps = json.loads((Path(tmp) / "apps.json").read_text())
            self.assertEqual(apps[0]["query_matches"], [])

    def test_nonempty_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "keep.txt"; existing.write_text("keep")
            with self.assertRaises(SystemExit), patch.object(c, "urlopen") as request:
                c.main(["--keyword", "music", "--output", tmp])
            request.assert_not_called()
            self.assertEqual(existing.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
