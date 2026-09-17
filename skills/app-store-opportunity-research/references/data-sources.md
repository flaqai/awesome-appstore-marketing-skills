# 数据采集与解释

## 公开数据优先级

1. Apple Search / Lookup API：应用身份、描述、分类、评分、价格、版本。接口参考 [Apple 官方存档文档](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/Searching.html)。该文档已归档，运行时结果与可用性需要验证。
2. 相同地区 App Store 页面：内购 SKU、截图、版本说明、可见评论；记录访问日期，抓取页可能滞后。
3. 开发者官网及帮助中心：能力说明、网站套餐、授权条款、官方移动应用链接。
4. 用户讨论或第三方商业估算：仅作为补充；标明样本/方法/时间及是否为估算，不能混为 Apple 数据。

请求形态：

```text
https://itunes.apple.com/search?term=ai+music&country=us&media=software&entity=software&limit=30
https://itunes.apple.com/lookup?id=6480136315&country=us&entity=software
https://itunes.apple.com/us/rss/customerreviews/page=1/id=6480136315/sortby=mostrecent/json
```

`software` 用于 iPhone 搜索，iPad 用 `iPadSoftware`，Mac 用 `macSoftware`。脚本支持 `--entity`，评论仍按应用 ID 归属。评论 RSS 是尽力获取的公开端点，不是完整评论 API；不可用不代表没有评论。分页上限 10，默认 1 页。部分应用内容和日期可能不完整。

## 脚本产物

- `manifest.json`：请求参数、采集开始/结束 UTC 时间、每个 URL、请求时间、成功/错误、响应文件及 SHA-256；`complete` 仅表示请求全部成功，不表示覆盖全部市场。
- `raw/*.json`：原始成功响应，供重放和复核。
- `apps.json`：按应用 ID 合并的候选池；保留全部搜索命中 `query_matches`、请求内位置、来源、官方分类、描述、评分、版本等；未人工筛选。
- `categories.json`：候选池中各官方主分类数量与应用 ID，不是市场份额或人工细分品类。
- `reviews.json`：保留 review ID、日期、星级、标题、内容、应用 ID、来源；不输出评论者名称。原始响应仍可能包含公开用户名。

程序按至少 3.2 秒的请求间隔串行调用，遇到网络错误、429 或 5xx 最多三次尝试，失败继续采集其他项。输出目录必须为空，避免把旧数据混入新调研。退出码 `0` 为请求成功，`2` 为有失败/部分数据，参数错误同样由命令行返回非零。不要仅凭退出码判断数据内容，应检查 manifest。

## 常见误读

- `averageUserRating` / `userRatingCount` 是此次地区响应的全版本评分指标；不是评论样本数、活跃用户或下载量。新版评分单独保留。
- `price=0` 只代表下载价；API 没给订阅价时不能从描述猜测。
- 搜索 `limit` 是请求上限，响应可能更少，且并非完整索引。无结果不能证明市场空白。
- 字段不存在时保存 `null`；空评分样本不参与均值比较。不同来源不要静默覆盖成一个数。
- 单次快照不证明增长；比较前后数据时保持地区、应用 ID、指标口径一致。

## 降级

接口失败时保留失败记录，使用可用浏览器或联网检索搜索 `site:apps.apple.com/<country>/app <keyword>`，打开具体应用页面并核对 ID。手工记录 URL、访问时间、查询、字段和缺失项；输出 `manual-evidence.json` 或 Markdown 证据表，不伪造 API 原始数据。工具只返回缓存页时注明其抓取日期。没有联网能力则只能交付研究框架及待采集清单。
