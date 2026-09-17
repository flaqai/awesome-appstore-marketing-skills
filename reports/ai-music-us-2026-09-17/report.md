# AI Music：美国 App Store 竞品与应用机会调研

调研日期：2026-09-17｜美国区 `us`｜iPhone｜中文报告｜公开信息桌面调研，未购买订阅或实机测试

## 结论

**建议先验证“已有歌曲的可控修改与交付”，再决定是否开发完整 AI 音乐应用。** 本轮观察到的供给已经覆盖整曲生成、翻唱、分轨、视频和社区；单纯增加一个文字生成歌曲入口，差异化依据不足。公开评分不能证明市场收入，但核心竞品的累计评分与近期评论，足以支持进一步做用户和产品验证。基础数据见[采集结果](data/apps.json)。

优先级是研究判断，不是市场规模排名：

1. **歌词、时长、声音保持一致的修改流程**：问题信号跨应用出现，值得最先测试。但 Suno 已发布相应编辑能力，需要证明可靠性或特定任务完成率上的优势。
2. **面向短视频创作者的配乐交付**：从完整生成流程收窄到定长、自然结尾、歌词视频和可导出文件；需求证据弱于第一项，先验证创作者工作流。
3. **纪念日/家庭故事的定制歌曲**：情绪价值有真实评论支持，可用按首交付测试；专门为此付费和持续获客尚未验证。

这些都是**待验证机会**，尚不足以宣称发现了确定的市场空白。下载量、收入、获客成本、留存率、关键词搜索量与市场增速本轮均未知。

## 1. 范围、覆盖与证据质量

API 采集于 **2026-09-17 06:35:04–06:35:43 UTC（北京时间 14:35）**。8 个关键词、每词请求上限 30，得到 224 条搜索命中、164 个去重候选应用；另抓取 5 款应用各 1 页近期评论，共 250 条，13 次请求全部成功。请求记录和原始响应校验值见 [manifest.json](data/manifest.json)。

本报告重点核查 **8 款应用**，同时保留相邻应用和待核实候选。164 是接口候选数，包含无关结果，不是 164 个直接竞品；没有穷尽市场。筛选状态见[候选记录](screening.json)，完整名称索引见[应用目录](app-catalog.md)。

评级、评分数、版本日期取同一轮 API；价格和关键功能补充自美国区商店页面，访问日期均为 2026-09-17。网页可能缓存或四舍五入，不能当作另一份增长快照。没有把搜索返回顺序当成 iPhone 搜索排名，也未使用网页偶尔显示的榜单位置来作市场判断。

评论使用 Apple RSS `mostrecent`，每款只取一页。实际最晚评论为 9 月 15 日，可能存在发布或缓存延迟。各应用覆盖时间不同，不能拿样本差评占比直接评定产品质量。记录的是评论数，未把它等同于独立用户数；跨页相同评论 ID 去重。可见文字不足以确认使用者真实性或评价中指控的事实。

## 2. 关键词与品类地图

### 检索词

| 检索词 | 目的 | 实际命中数 |
|---|---|---:|
| ai music | 核心供给发现 | 28 |
| ai song generator | 文本/歌词到整曲 | 28 |
| ai cover | 翻唱、声音替换 | 25 |
| background music maker | 配乐与视频制作替代方案 | 29 |
| stem splitter | 分轨、伴奏、练习工作流 | 30 |
| Suno | 品牌补充与同名身份检查 | 28 |
| Mureka | 品牌补充与相关生成应用 | 30 |
| Endel | 功能性音乐、专注与睡眠场景 | 26 |

每个应用保留命中词及请求内位置，可在 [apps.json](data/apps.json) 的 `query_matches` 复查。品牌词会带来选择偏差；下一轮应为选中的细分方向补充任务词，例如 `change song lyrics`、`music for reels`、`personalized birthday song`，验证这轮尚未覆盖的专门竞品。

### 官方分类与分析赛道分别看

候选池的官方主分类：Music 112、Health & Fitness 19、Photo & Video 11、Productivity 7、Utilities 6、Entertainment 4、Medical 2、Lifestyle 1、Education 1、Finance 1。这个分布仅描述本次检索结果；后两类也说明搜索有噪声。见[官方分类数据](data/categories.json)。

| 人工分析赛道 | 用户要完成的任务 | 代表应用 | 相关官方分类 | 与整曲生成的关系 |
|---|---|---|---|---|
| 整曲生成与创作 | 把想法、歌词或录音变成完整歌曲 | Suno、Donna、Mureka、Udio、MyTunes | Music | 直接竞品 |
| AI 翻唱与声音替换 | 用指定声音重唱或改编 | Banger、MyTunes、Donna；VocalMe 待深挖 | Music；候选亦有 Entertainment | 交叉竞争 |
| 歌曲编辑与分轨 | 提取伴奏、变速、改调、练习 | Moises；Stemz、Splitteroo 待深挖 | Music；候选亦有 Utilities | 下游/相邻竞品 |
| 配乐与音乐视频 | 把音乐用于短视频或制作歌词视频 | Mureka、MyTunes、Donna；Shoom、视频配乐工具待深挖 | Music、Photo & Video | 交付任务交叉 |
| 个性化收听 | 听自己的 AI 歌曲或社区作品 | Mureka、Suno | Music | 平台消费侧 |
| 专注/睡眠声音 | 在特定情境持续收听适配声音 | Endel；Brain.fm、Calm 作为替代方案待深挖 | Health & Fitness、Productivity | 相邻市场，用户目标不同 |

上述映射依据应用描述作研究分类，不是 Apple 官方细分类，也不代表所有同名应用采用同一种 AI 技术。事实来源见[应用数据](data/apps.json)和下文各应用商店链接。

## 3. 核心竞品概览

评分四舍五入至两位小数，评分数保留接口整数。全部 8 款下载价为 **USD 0**；收费功能另见内购表。版本日期为 UTC 日期。

| 应用 / ID | 开发者 | 官方主分类 | 评分 / 评分数 | 版本 / 更新日期 | 角色 |
|---|---|---|---|---|---|
| [Suno - AI Songs, Music, Lyrics](https://apps.apple.com/us/app/suno-ai-songs-music-lyrics/id6480136315)<br>6480136315 | Suno, Inc. | Music | 4.89 / 349,116 | 1.88.0 / 2026-09-09 | 直接：整曲/编辑基准 |
| [Donna AI Song & Music Maker](https://apps.apple.com/us/app/donna-ai-song-music-maker/id6482289804)<br>6482289804 | Mobiversite（完整名称见下） | Music | 4.74 / 94,918 | 1.0.98 / 2026-09-11 | 直接：生成/翻唱/视频 |
| [Mureka: AI Radio & Music Maker](https://apps.apple.com/us/app/mureka-ai-radio-music-maker/id6677033144)<br>6677033144 | SKYWORK AI PTE LTD | Music | 4.79 / 10,866 | 1.51.1 / 2026-09-03 | 直接：创作/收听 |
| [MyTunes : AI Music Generator](https://apps.apple.com/us/app/mytunes-ai-music-generator/id6447001239)<br>6447001239 | HUBX | Music | 4.32 / 39,617 | 2.5.0 / 2026-08-25 | 直接：生成/声音 |
| [Banger: AI Music Generator](https://apps.apple.com/us/app/banger-ai-music-generator/id6452017015)<br>6452017015 | 42 Digital | Music | 4.39 / 41,049 | 9.9 / 2026-06-10 | 直接：翻唱/生成 |
| [Udio: AI Music Maker & Studio](https://apps.apple.com/us/app/udio-ai-music-maker-studio/id6511211165)<br>6511211165 | Uncharted Labs Inc. | Music | 4.21 / 3,441 | 0.22.0 / 2026-08-20 | 直接：创作/编辑 |
| [Moises: The Musician's App](https://apps.apple.com/us/app/moises-the-musicians-app/id1515796612)<br>1515796612 | Moises Systems, Inc | Music | 4.70 / 27,743 | 2.145.0 / 2026-09-15 | 相邻：分轨/练习 |
| [Endel: Focus & Sleep Sounds](https://apps.apple.com/us/app/endel-focus-sleep-sounds/id1346247457)<br>1346247457 | Endel | Health & Fitness | 4.64 / 33,769 | 4.8.8 / 2026-09-03 | 相邻：功能性声音 |

Donna 开发者栏为简称；API 完整卖方名称为 MOBIVERSITE YAZILIM BILISIM REKLAM VE DANISMANLIK HIZMETLERI SANAYI TICARET LIMITED STI。其余完整卖方、bundle ID、兼容设备、语言、应用描述与来源都在 [apps.json](data/apps.json)。

**选样理由：** Suno 为本轮整曲生成样本中评分积累最大的参照；Donna、MyTunes、Banger 体现生成和翻唱功能交叉；Mureka 覆盖创作与收听；Udio 是较小评分量但功能完整的直接竞品；Moises 和 Endel 用来划清相邻用户任务。不能因 Udio iOS 评分少，就认为整个品牌规模小。

**扩展观察：** MusicGPT（ID 6743325248，1,235 个评分）和 Beats（ID 6783634629，15 个评分）进入待深挖清单；低评分数量既可能来自新品，也可能是低采用率，不等于蓝海。Shoom、Muzio、Soniva、Zona、Mozart、VocalMe 等也保留在候选目录，尚未逐一核验套餐和评论。

**身份与排除：** `Suno Studio: AI Song Generator`（6770908796，BAFFOE HAIR SALON (PTY) LTD）和 `AI Music by Suno Studio`（6771736157，TOY CASTLE SDN. BHD.）与 Suno（6480136315，Suno, Inc.）开发者不同，不能合并或认作官方应用，本轮置为身份待核实。`单词争霸`、STRIKE 比特币应用不属于本轮任务。ChatGPT、Google Gemini 暂不进入核心独立音乐应用表；这不代表它们没有音乐相关能力。证据来自同轮[搜索响应](data/manifest.json)。

## 4. 功能与商业化

### 能力矩阵

“宣称”指官方描述/帮助文档明确提及，尚未实测；“未提及”不等于没有。网站说明与移动端能力有差异时单独列出。

| 应用 | 创建方式 | 修改与控制 | 输出/下游 | 判断意义 |
|---|---|---|---|---|
| [Suno](https://apps.apple.com/us/app/suno-ai-songs-music-lyrics/id6480136315) | 文本、歌词、录音/哼唱 | 宣称可编辑结构、声音；v6 帮助文档进一步列出局部编辑 | 移动端 MP3；WAV 的官方说明指向网页，下载有套餐限制 | 能力全面，可控修改机会必须以实测胜出 |
| [Donna](https://apps.apple.com/us/app/donna-ai-song-music-maker/id6482289804) | 文本/歌词到歌曲、自己的声音 | 宣称延长、分轨 | 宣称音乐视频；商店列有相关内购 | “加视频/分轨”本身已有竞争 |
| [Mureka](https://apps.apple.com/us/app/mureka-ai-radio-music-maker/id6677033144) | 文本、图片、视频到音乐 | 宣称声音/风格控制与重混 | 创作、社区、场景电台；针对内容创作者的配乐定位 | 已跨入视频配乐人群 |
| [MyTunes](https://apps.apple.com/us/app/mytunes-ai-music-generator/id6447001239) | 歌词/提示词生成、声音及翻唱 | 声音变换；精确锁定编辑待核实 | 宣称音乐视频；样本存在保存/分享异常反馈 | 最终交付可靠性值得测试 |
| [Banger](https://apps.apple.com/us/app/banger-ai-music-generator/id6452017015) | 提示词生成、AI 翻唱 | 宣称替换声音并保留旋律 | 宣称保存和分享 | 翻唱已是成熟供给方向之一 |
| [Udio](https://apps.apple.com/us/app/udio-ai-music-maker-studio/id6511211165) | 文本、Pro 音频上传 | 宣称逐行歌词编辑、延长、模型控制 | **来源冲突：商店称可导出，官方帮助中心称下载已禁用** | 不可直接按商店描述标为可用导出工具 |
| [Moises](https://apps.apple.com/us/app/moises-the-musicians-app/id1515796612) | 导入已有音频/视频 | 分轨、变速、改调、和弦、循环 | 分轨/混音导出；描述将 WAV 标为桌面端 | 音乐练习工作流，区别于整曲创作 |
| [Endel](https://apps.apple.com/us/app/endel-focus-sleep-sounds/id1346247457) | 情境适配声音 | 专注计时、声音场景选择 | 个性化与离线收听；歌曲交付未提及 | 不是直接卖“生成一首歌”的竞品 |

**影响判断的两项复核：**

- Suno 的 2026-09-09 官方说明确认旧模型退休，新迭代使用 v6 家族，并宣称支持局部歌词修改。本轮 9 月评论处于模型切换后，不能把相关不满直接解释为长期趋势。修改能力已经存在，因此第一优先方向的验证目标是完成质量与重复成本。[v6 FAQ](https://help.suno.com/en/articles/13924481)
- Udio 商店描述仍写有音视频导出，而 2026-02-17 的官方帮助文章明确说明音频、视频和分轨下载被禁用。报告保留冲突，以限制更明确的帮助说明作保守判断；未实机核实恢复情况。[Udio 帮助说明](https://help.udio.com/en/articles/12683565-changes-associated-with-the-universal-music-group-umg-partnership)

### 美国区可见内购示例

金额为 USD。以下是页面可见条目，不保证是当前所有新用户展示的价格；未标周期的项目不推定月/年。同一套餐有多个价位，可能涉及不同优惠或产品条目，本轮无法确定原因。

| 应用 | 可见产品条目与价格 | 解释与缺口 |
|---|---|---|
| [Suno](https://apps.apple.com/us/app/suno-ai-songs-music-lyrics/id6480136315) | Pro Plan $10 / $96；Premier Plan $30 / $289；500 Credits $4；1 Download Credit $2.99 / $4.99 | 内购清单没为每项标周期；生成额度和下载额度是不同约束 |
| [Donna](https://apps.apple.com/us/app/donna-ai-song-music-maker/id6482289804) | 1 Week PRO $5.99；1 Week Pro $2.99；1 Year PRO $59.99；AI Cover $5.99；AI Music Video Small $5.99 | 周/年套餐与额外功能并存，不能仅比较订阅价 |
| [Mureka](https://apps.apple.com/us/app/mureka-ai-radio-music-maker/id6677033144) | Monthly Pro plan $9 / $10；Monthly Premier plan $27；Yearly Pro plan $79.99；4,000 Gold $18 | 同名月套餐有不同价格，适用范围待核实 |
| [MyTunes](https://apps.apple.com/us/app/mytunes-ai-music-generator/id6447001239) | Weekly Subscription $9.99 / $6.99；Yearly subscription $39.99；Custom Voice $4.99 | 订阅与自定义声音条目分别列出 |
| [Banger](https://apps.apple.com/us/app/banger-ai-music-generator/id6452017015) | Unlimited Premium $6.99 / $39.99；Credit Pack - Medium $9.99 | “Unlimited”与积分包同时出现，实际覆盖范围待实测 |
| [Udio](https://apps.apple.com/us/app/udio-ai-music-maker-studio/id6511211165) | Udio Standard - Monthly $10；Udio Pro - Monthly $30；Udio Standard - Annual $96 | 价格证据不能解决上述导出限制冲突 |
| [Moises](https://apps.apple.com/us/app/moises-the-musicians-app/id1515796612) | Moises Premium - Monthly $5.99；Moises Premium - Yearly $39.99；Moises Pro - Monthly $29.99 | 免费、Premium、Pro 的工具范围不同 |
| [Endel](https://apps.apple.com/us/app/endel-focus-sleep-sounds/id1346247457) | 1 Month $19.99 / $2.99 / $7.49；12 Months $119.99 / $34.99 / $59.99 | 不使用最低展示价代表所有用户可买价格 |

Suno 当前帮助说明将 Pro/Premier 的普通歌曲下载分别列为每月 20/60 次；免费计划最多提供 7 次终身试用下载，Studio 工作流另有例外。同一歌曲多格式不重复计数。这说明应比较“可交付成果成本”，不能只用“每月生成多少首”衡量价值。[下载额度](https://help.suno.com/en/articles/13926209)、[文件格式与平台](https://help.suno.com/en/articles/13926081)

商店收费体现开发者的定价方式，不等于真实付费意愿或收入。商用授权、客户可否再分发、声音授权和生成服务成本仍需按最终所选供应商的当前条款核实；本轮未完成逐套餐授权审查。Mureka 商店的免版税定位属于开发者宣称，未在此提升为法律结论。

## 5. 评论样本与问题证据

### 样本口径

以下按源评论时间的日期部分展示，完整时间与时区见 [reviews.json](data/reviews.json)。排序为近期，不是低分优先；未从网页精选评论补入分母。

| 应用 | 评论数 | 1★ / 2★ / 3★ / 4★ / 5★ | 样本日期范围 |
|---|---:|---|---|
| Suno - AI Songs, Music, Lyrics | 50 | 9 / 1 / 2 / 3 / 35 | 2026-09-13 – 2026-09-15 |
| Donna AI Song & Music Maker | 50 | 8 / 1 / 0 / 7 / 34 | 2026-08-25 – 2026-09-15 |
| Mureka: AI Radio & Music Maker | 50 | 12 / 5 / 4 / 4 / 25 | 2026-02-15 – 2026-09-14 |
| MyTunes : AI Music Generator | 50 | 4 / 2 / 6 / 2 / 36 | 2026-09-12 – 2026-09-15 |
| Banger: AI Music Generator | 50 | 4 / 2 / 2 / 12 / 30 | 2026-07-30 – 2026-09-15 |

多数样本给出四/五星，同时部分高分评论也包含具体问题。尤其 Mureka 的 50 条跨越约七个月，而 Suno/MyTunes 只跨几天；不能比较这些样本的投诉比例来推断谁更差。

### 人工核查的主题证据

下表是**已逐条核查的证据子集**，不是对全部 250 条完成穷尽编码后的发生率。同一条评论可能有多个主题；不同主题的计数不能相加当作用户数。所有标识、日期、应用 ID、星级及来源 URL 见 [review-evidence.json](review-evidence.json)。

| 主题 | 已核查命中 | 代表评论及摘要 | 对方向的意义 |
|---|---|---|---|
| 指令与成品不一致 | 5 款应用、11 条 | Suno `14547128644`；Donna `14528914094`；Mureka `14009017547`；MyTunes `14551034426`；Banger `14539233726`：涉及歌词、风格、人声或重复尝试仍不满足要求 | 可控输出是跨产品问题线索；不能由此证明新团队能解决 |
| 时长与自然结尾 | 4 款应用、4 条 | Suno `14551149657`、Donna `14528914094`、Mureka `13817644488`、MyTunes `14545373745`：时长、截断或收尾与预期不符 | 可用具体定长任务测试，容易定义验收标准 |
| 保存/分享可靠性 | 1 款应用、3 条 | MyTunes `14549988533`、`14546333056`、`14552510313`；最后一条为四星，评论者承认也可能是自身问题 | 是故障线索，尚未证明所有用户受影响 |
| 创作版本管理被推荐内容打断 | 1 款应用、1 条 | Suno `14553502770`：付费创作者希望自己的多个版本连续集中展示 | 细分专业工作流线索，目前仅单点证据 |
| 歌词视频与发布 | 1 款应用、1 条 | Mureka `14288044787`：五星评价仍希望有简单歌词视频及上传 YouTube 的流程 | 支持配乐交付实验，不能证明竞品完全缺少视频能力 |
| 创作满足感与家庭记忆 | 5 款应用、5 条 | Banger `14531595211`：把家人留下的歌词变成歌曲；Suno `14554809018`：故事与角色配乐；Donna、MyTunes、Mureka 有表达和创作乐趣的正反馈 | 除生产效率外，也存在具体情绪价值 |

费用相关反馈另保留三个具体例子：Donna `14484503935`、MyTunes `14548879209`、Mureka `13902992691`。它们说明有用户对额外积分、计价或扣减预期不一致，但尚未独立验证扣费行为。不能把“不想付费”解释成“愿意为更便宜竞品付费”。来源为各应用 [RSS 请求与原始响应](data/manifest.json)。

## 6. 优先验证的三个方向

### 方向一：面向反复改歌者的可控修改与版本比较

**用户任务：** 已生成大致满意的歌曲，希望只改一句歌词、歌手或结尾，并保留其余满意部分。观察依据是上文跨应用指令一致性主题，以及同一首歌重复修改的具体反馈。

**机会假设：** 有一小群高频创作者愿意为更少无效重做、更稳定的结果和清楚的版本比较付费。最小产品可从“导入用户有权使用的作品 → 选择需修改片段 → 保存原版 → A/B 对照 → 验收导出”开始。身份、模型和歌词版本可追溯，失败时明确展示结果和计费状态。

**反证：** Suno 已有局部编辑与新模型；Udio 宣称逐行歌词与项目组织；Moises 已覆盖部分后期处理。仅做提示词包装或增加一个文件夹不足以形成优势。跨模型保持音色/旋律可能受底层能力限制，不能靠界面承诺解决。

**一周内实验：** 招募 10 名最近实际改过歌的创作者，各拿 3 个真实修改任务，以当前竞品作为基线做同任务对照。先用人工服务与简单原型测流程，不先自研模型。预设继续条件：30 个任务中至少 21 个在不破坏指定保留片段的情况下验收，完成时间中位数相对基线减少至少 30%，且至少 4 人愿意为下一批真实任务付费。若竞品原生功能即可达到同等结果，或必须整体重生成导致核心保留条件失败，则停止该切口。这些阈值是实验设计假设，尚未产生测试结果。

**获客假设与依赖：** 从 AI 歌曲创作者社群的真实修改前后演示找首批用户；需可用且获授权的编辑服务，测算重试成本。方向优先级高；痛点信心中，技术优势与商业信心低。

### 方向二：短视频创作者的定长配乐与交付包

**用户任务：** 为一条短片得到 15/30/60 秒、不截断歌词、有自然收尾、能正确导出的音乐与歌词视频。问题线索来自时长、保存与歌词视频主题；当前样本未确认提出这些问题的人都是商业短视频创作者。

**机会假设：** 对创作者而言，“能立即放进成片”比“再生成一首完整歌曲”更值得付费。最小交付只包含选择时长、确定情绪、审核歌词、自然收尾和导出。授权信息只按所用服务真实条款展示，不自称无版权风险。

**反证：** Mureka 已定位内容创作者，Donna/MyTunes 已宣称视频能力；视频编辑器、素材库和人工剪辑也是替代方案。本轮 `background music maker` 不足以覆盖全部短视频配乐竞品，下一轮必须补查视频编辑器和专用配乐工具。

**实验：** 8 名有近期发布记录的创作者提供共 20 条视频任务，比较现有工具与人工辅助交付。继续条件设为至少 14 条音乐被用于真实成片、至少 3 人愿意为第二批任务付费；若多数用户用现有素材库更快，或实际可用授权/每次交付成本不可接受，则停止。首批可通过一种垂直视频类型招募，如产品展示短片，避免一开始覆盖所有创作者。

方向优先级中；任务信心中低，付费与获客信心低。

### 方向三：家庭故事与纪念日定制歌曲

**用户任务：** 将个人记忆、家人歌词或祝福制作成可赠送的歌。家人歌词的具体案例与跨应用的创作乐趣反馈，支持做情绪价值验证；它们没有证明一个独立纪念日应用的需求规模。

**机会假设：** 用场景问答、名字发音确认、歌词审核、固定交付时间和礼物卡片，降低用户反复试提示词的成本。先按首/按场景服务测试定价，报价是自有实验变量，不套用竞品订阅费。

**反证：** 通用生成器已能根据祝福写歌，差异可能只在模板和交付服务；节庆任务低频，获客成本和退款/重做成本可能吞掉利润。语音和家人素材应只使用用户获授权提供的内容。

**实验：** 招募 10 名未来两周有真实赠礼场景的人，提供试听后选择付费交付。继续条件设为至少 3 个实际订单、至少 2 个自然转介绍意愿，并记录每单修改次数、耗时及毛利；无人购买或全部价值来自高成本人工创作时停止软件化。先验证交付价值，再决定要不要做 iOS 应用。

方向优先级中低；情绪价值信心中，独立产品与复购信心低。

## 7. 下一步与边界

建议先执行方向一的同任务对照，同时用少量访谈判断方向二是否更符合目标用户。建立 30 个固定测试任务，记录成功率、保留条件、重复生成次数、实际支付与导出结果，而不是只收集“听起来不错”的反馈。

下一轮需补齐：选定切口的专用关键词与小产品；Udio 当前可用功能；8 款应用的真实付费墙与导出体验；至少 2 款候选底层服务的授权和成本；相同地区的第二次时间快照。未经这些验证，不估算利润，不承诺产品方向已经成立。

本轮没有安装/付费体验竞品、没有采集完整历史评论、没有商业估算数据源、没有判断模型训练来源或所有权。评论里的旧版本问题可能已修复；官方描述也可能滞后，已发现的冲突在功能矩阵显式保留。

## 8. 数据与复现

- [请求清单、时间和原始响应校验值](data/manifest.json)
- [164 个候选应用及每个检索词的命中记录](data/apps.json)
- [官方主分类统计](data/categories.json)
- [250 条去重评论](data/reviews.json)
- [人工筛选状态](screening.json)与[应用目录](app-catalog.md)
- [人工核查的评论主题证据](review-evidence.json)
- [网页证据与冲突记录](web-evidence.json)

复现公开接口采集（使用新的输出目录，结果会随时间变化）：

```bash
python3 skills/app-store-opportunity-research/scripts/collect_app_store.py \
  --keyword 'ai music' --term 'ai song generator' --term 'ai cover' \
  --term 'background music maker' --term 'stem splitter' \
  --term 'Suno' --term 'Mureka' --term 'Endel' \
  --country us --limit 30 \
  --review-app-id 6480136315 --review-app-id 6482289804 \
  --review-app-id 6677033144 --review-app-id 6447001239 \
  --review-app-id 6452017015 --output reports/ai-music-new-run/data
```

采集器只生成公开数据与来源记录；本报告的筛选、比较、冲突处理和机会判断由研究者完成。流程理念参考 [froessell/app-store-opportunity-research](https://github.com/froessell/app-store-opportunity-research)，本报告使用独立采集数据与当前官方页面。
