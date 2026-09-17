# awesome-appstore-marketing-skills
Awesome Skills for marketing in App Store. Explore the skills for both app trends or ASO in App Store.

## Skills

| Skill | 用途 | 实测示例 |
|---|---|---|
| [app-store-opportunity-research](skills/app-store-opportunity-research/SKILL.md) | 输入关键词，发现相关品类与应用，采集评分、版本、描述及评论，输出竞品矩阵和机会判断 | [AI Music 美国区竞品调研](reports/ai-music-us-2026-09-17/report.md) |

## 使用

在支持本地技能的助手中加载 `skills/app-store-opportunity-research/SKILL.md`，例如：

> 使用这个 skill，研究美国 App Store 的 ai music 方向。扩展相关关键词，区分整曲生成、翻唱、配乐和分轨应用，给我中文竞品报告与优先验证的机会。

技能安装到助手的技能目录后，可用 `$app-store-opportunity-research` 调用。当前仓库保存的是可分发技能源码。

公开数据采集仅依赖 Python 3.9+ 和联网环境，不需要 API key：

```bash
python3 skills/app-store-opportunity-research/scripts/collect_app_store.py \
  --keyword "ai music" --term "ai song generator" --term "ai cover" \
  --country us --limit 30 --output reports/my-research/data
```

采集器输出候选应用、官方分类、原始响应及请求记录；相关性筛选、内购核实与机会分析由技能指导助手完成。更多参数见[数据采集说明](skills/app-store-opportunity-research/references/data-sources.md)。

生成的报告及采集数据统一保存在 `reports/`。仓库保留 `reports/ai-music-us-2026-09-17/` 作为完整示例，包含报告及其引用的数据；后续调研请使用新目录，默认由 `.gitignore` 排除，仅保留在本地。

运行采集逻辑检查：

```bash
python3 -m unittest discover -s tests -v
```

## 来源

研究流程理念参考 [froessell/app-store-opportunity-research](https://github.com/froessell/app-store-opportunity-research)。本仓库独立实现关键词采集与证据分析，不复制原项目文本或收入估算规则。应用和评论数据来自 Apple 公开接口，相关内容权利归原权利人；示例数据是注明日期的调研快照，不代表完整市场或当前实时状态。
