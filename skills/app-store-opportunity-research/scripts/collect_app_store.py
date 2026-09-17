#!/usr/bin/env python3
"""Read-only App Store research collector; Python 3.9+, standard library only."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def label(item, key):
    value = item.get(key, {})
    return value.get("label") if isinstance(value, dict) else None


def normalize_app(item, country):
    keys = (
        "trackId", "trackName", "bundleId", "artistName", "artistId", "sellerName",
        "trackViewUrl", "sellerUrl", "primaryGenreName", "primaryGenreId", "genres",
        "genreIds", "averageUserRating", "userRatingCount", "averageUserRatingForCurrentVersion",
        "userRatingCountForCurrentVersion", "price", "currency", "formattedPrice",
        "version", "releaseDate", "currentVersionReleaseDate", "releaseNotes", "description",
        "minimumOsVersion", "supportedDevices", "languageCodesISO2A", "fileSizeBytes",
        "contentAdvisoryRating", "screenshotUrls", "ipadScreenshotUrls", "artworkUrl512",
    )
    result = {key: item.get(key) for key in keys}
    result.update(storefront=country, query_matches=[], sources=[])
    return result


def add_apps(apps, payload, country, source, query=None):
    for position, item in enumerate(payload["results"], 1):
        app_id = item.get("trackId")
        if app_id is None or item.get("wrapperType") != "software":
            continue
        key = str(app_id)
        if key not in apps:
            apps[key] = normalize_app(item, country)
        app = apps[key]
        # Keep first snapshot; raw responses preserve any later discrepancies.
        if source not in app["sources"]:
            app["sources"].append(source)
        if query is not None:
            app["query_matches"].append({"term": query, "response_position": position, "source_url": source})


def parse_reviews(payload, app_id, country, source):
    entries = payload["feed"].get("entry", [])
    if isinstance(entries, dict):
        entries = [entries]
    reviews = []
    for item in entries:
        rating = label(item, "im:rating")
        if rating is None:  # Some feeds include an app metadata entry.
            continue
        review_id = label(item, "id")
        if review_id is None:
            continue
        reviews.append({
            "review_id": str(review_id), "app_id": str(app_id), "storefront": country,
            "rating": int(rating), "title": label(item, "title"),
            "content": label(item, "content"), "updated": label(item, "updated"),
            "version": label(item, "im:version"), "source_url": source,
        })
    return reviews


class Collector:
    def __init__(self, output, interval=3.2):
        self.output = output
        self.interval = interval
        self.last_request = None
        self.requests = []

    def fetch(self, url, kind, **context):
        record = {"url": url, "kind": kind, **context, "requested_at": utc_now(), "attempts": 0}
        self.requests.append(record)
        for attempt in range(3):
            if self.last_request is not None:
                time.sleep(max(0, self.interval - (time.monotonic() - self.last_request)))
            self.last_request = time.monotonic()
            record["attempts"] += 1
            try:
                request = Request(url, headers={"User-Agent": "AppStoreOpportunityResearch/1.0", "Accept": "application/json"})
                with urlopen(request, timeout=30) as response:
                    body = response.read()
                payload = json.loads(body)
                if not isinstance(payload, dict):
                    raise ValueError("Response must be a JSON object")
                if kind in ("search", "lookup"):
                    if not isinstance(payload.get("results"), list):
                        raise ValueError("Missing results array")
                    if not all(isinstance(item, dict) for item in payload["results"]):
                        raise ValueError("Invalid result item")
                elif not isinstance(payload.get("feed"), dict):
                    raise ValueError("Missing review feed")
                filename = "raw/{:03d}-{}.json".format(len(self.requests), kind)
                (self.output / filename).write_bytes(body)
                record.update(status="ok", fetched_at=utc_now(), raw_file=filename,
                              sha256=hashlib.sha256(body).hexdigest())
                if kind in ("search", "lookup"):
                    record["result_count"] = len(payload["results"])
                return payload
            except HTTPError as exc:
                error = "HTTP {}".format(exc.code)
                retry = exc.code == 429 or 500 <= exc.code < 600
            except (URLError, TimeoutError, OSError) as exc:
                error, retry = str(exc), True
            except (ValueError, TypeError) as exc:
                error, retry = str(exc), False
            if not retry or attempt == 2:
                break
            time.sleep(2 ** attempt * 3.2)
        record.update(status="error", error=error, finished_at=utc_now())
        print("Request failed: {} ({})".format(url, error), file=sys.stderr)
        return None


def positive_id(value):
    if not re.fullmatch(r"[1-9][0-9]*", value):
        raise argparse.ArgumentTypeError("App ID must be a positive integer")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--term", action="append", default=[])
    parser.add_argument("--country", default="us", help="Two-letter storefront code")
    parser.add_argument("--entity", choices=["software", "iPadSoftware", "macSoftware"], default="software")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--app-id", action="append", default=[], type=positive_id)
    parser.add_argument("--review-app-id", action="append", default=[], type=positive_id)
    parser.add_argument("--review-pages", type=int, default=1)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    country = args.country.lower()
    if not re.fullmatch(r"[a-z]{2}", country):
        parser.error("--country must be a two-letter storefront code")
    if not args.keyword.strip() or any(not term.strip() for term in args.term):
        parser.error("Search terms must not be blank")
    if not 1 <= args.limit <= 200 or not 1 <= args.review_pages <= 10:
        parser.error("--limit must be 1..200 and --review-pages must be 1..10")
    output = args.output
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error("--output must be a new or empty directory")
    (output / "raw").mkdir(parents=True, exist_ok=True)
    terms = list(dict.fromkeys(term.strip() for term in [args.keyword] + args.term))
    manifest = {
        "schema_version": 1, "started_at": utc_now(), "keyword": args.keyword,
        "storefront": country, "entity": args.entity, "limit": args.limit, "terms": terms,
        "lookup_app_ids": list(dict.fromkeys(args.app_id)),
        "review_app_ids": list(dict.fromkeys(args.review_app_id)), "review_pages": args.review_pages,
        "complete": False,
        "limitations": ["Candidate pool is not relevance-filtered or exhaustive.",
                        "Response position is not an App Store search or chart rank.",
                        "Ratings are not downloads, revenue, or sampled review counts.",
                        "Review RSS is a recent, incomplete, non-random sample."],
    }
    save_json(output / "manifest.json", manifest)
    collector = Collector(output)
    apps, reviews = {}, {}
    for term in terms:
        url = "https://itunes.apple.com/search?" + urlencode({
            "term": term, "country": country, "media": "software", "entity": args.entity, "limit": args.limit,
        })
        payload = collector.fetch(url, "search", term=term)
        if payload is not None:
            add_apps(apps, payload, country, url, query=term)
    for app_id in manifest["lookup_app_ids"]:
        url = "https://itunes.apple.com/lookup?" + urlencode({"id": app_id, "country": country, "entity": args.entity})
        payload = collector.fetch(url, "lookup", app_id=app_id)
        if payload is not None:
            add_apps(apps, payload, country, url)
    for app_id in manifest["review_app_ids"]:
        for page in range(1, args.review_pages + 1):
            url = "https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/sortby=mostrecent/json".format(country, page, app_id)
            payload = collector.fetch(url, "reviews", app_id=app_id, page=page)
            if payload is None:
                break
            try:
                batch = parse_reviews(payload, app_id, country, url)
            except (ValueError, TypeError, AttributeError, KeyError) as exc:
                collector.requests[-1].update(status="error", error="Review parse error: " + str(exc))
                break
            collector.requests[-1]["review_count"] = len(batch)
            for review in batch:
                reviews[(app_id, review["review_id"])] = review
            if not batch:
                break
    app_list = sorted(apps.values(), key=lambda app: app["trackId"])
    categories = Counter(app["primaryGenreName"] or "Unknown" for app in app_list)
    category_list = [{"primary_genre": name, "candidate_count": count,
                      "app_ids": [a["trackId"] for a in app_list if (a["primaryGenreName"] or "Unknown") == name]}
                     for name, count in categories.most_common()]
    save_json(output / "apps.json", app_list)
    save_json(output / "categories.json", category_list)
    save_json(output / "reviews.json", list(reviews.values()))
    failures = sum(record["status"] != "ok" for record in collector.requests)
    manifest.update(finished_at=utc_now(), requests=collector.requests, unique_app_count=len(apps),
                    review_count=len(reviews), failed_request_count=failures, complete=failures == 0)
    save_json(output / "manifest.json", manifest)
    print(json.dumps({"output": str(output), "apps": len(apps), "reviews": len(reviews), "failed_requests": failures}))
    return 2 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
