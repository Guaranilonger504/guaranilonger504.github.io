# Shiori Route

Shiori Route 是一个极简的中英双语 Hugo 个人网站，并包含每天自动运行的
“研究论文雷达”。GitHub Pages 只展示静态文件；论文抓取和 OpenAI 调用只发生在
本地 Python 脚本或 GitHub Actions 中。

> 论文雷达的分析仅基于标题和摘要，可能存在错误，请始终以论文原文为准。

## 架构

```text
arXiv Atom API
  → 日期/分类过滤
  → JSON 状态去重
  → OpenAI 批量初筛（Structured Outputs）
  → 高分论文深入分析（仍仅基于标题和摘要）
  → 双语 Hugo Markdown + JSON + RSS
  → Git commit
  → 现有 Pages workflow 构建并发布
```

网站由 `hugo.toml`、`layouts/`、`static/` 和 `content/` 构成。论文雷达由：

- `config/paper-radar.yaml`：分类、研究兴趣、模型、阈值和成本上限。
- `paper_radar/`：抓取、解析、去重、分析和确定性输出逻辑。
- `scripts/paper_radar.py`：命令行入口。
- `data/processed_papers.json`：跨 Action 运行保存的可读状态。
- `.github/workflows/paper-radar.yaml`：每日内容更新。
- `.github/workflows/pages.yaml`：已有的 Hugo Pages 发布流程。

## 研究筛选标准

系统优先寻找 MPC、secure computation、MP-SPDZ、MPC compiler/runtime、WAN
latency、通信轮次、dependency DAG、batching、pipeline、network-aware runtime
和 secure LLM inference 相关论文。

它也会主动关注分布式 runtime、数据流/查询/编译器调度、critical path、adaptive
batching、latency hiding、collective communication、性能模型和 LLM serving，
判断这些机制是否可能迁移到 MPC runtime。纯应用替换、通用区块链、入侵检测和
图像水印默认低优先级。

## 本地安装

需要安装 [uv](https://docs.astral.sh/uv/) 和 Docker：

```bash
uv sync
uv run pytest
docker compose up
```

网站预览地址为 <http://localhost:1313>。

## OpenAI API Key

本地运行前只在当前 shell 中设置环境变量，不要写入文件：

```bash
export OPENAI_API_KEY="your-key"
uv run python scripts/paper_radar.py --analyze
```

脚本使用官方 OpenAI Python SDK 和 Pydantic Structured Outputs。Key 不会进入
请求内容、日志或生成文件。

在 GitHub 仓库中进入 **Settings → Secrets and variables → Actions → New
repository secret**，创建名为 `OPENAI_API_KEY` 的 Secret。

## 本地命令

```bash
# 同步环境
uv sync

# 运行离线测试
uv run pytest

# 抓取并显示预计数量；不调用 OpenAI、不写文件
uv run python scripts/paper_radar.py --dry-run

# 只抓取；不调用 OpenAI、不写文件
uv run python scripts/paper_radar.py --fetch-only

# 完整分析
uv run python scripts/paper_radar.py --analyze

# 指定运行日期（UTC）
uv run python scripts/paper_radar.py --analyze --date 2026-07-25

# 使用测试 fixture 验证抓取和 dry-run，不访问 arXiv
uv run python scripts/paper_radar.py --dry-run --fixture tests/fixtures/arxiv.xml --date 2026-07-25
```

`--dry-run` 和 `--fetch-only` 都不会调用 OpenAI，也不会写正式产物。

## GitHub Actions

`Daily paper radar` 每天 `21:17 UTC` 运行，对应次日日本时间 `06:17 JST`。
选择非整点是为了避开 GitHub Actions 定时任务的拥堵时段。它也支持
**Actions → Daily paper radar → Run workflow** 手动触发。

工作流依次执行：

1. 安装 uv 和 Python。
2. 从锁文件安装依赖。
3. 运行离线测试。
4. 抓取和分析论文。
5. 使用固定 Hugo Docker 镜像验证网站。
6. 仅当生成内容或状态有变化时提交并 push。
7. push 触发现有 `Build and deploy Hugo` 工作流发布 Pages。

工作流只由 `schedule` 和 `workflow_dispatch` 触发，不处理 fork pull request，
因此 fork PR 无法获得 OpenAI Secret。并发组会避免两次雷达任务同时运行。

## 成本控制

所有限制都在 `config/paper-radar.yaml`：

- 最多抓取 100 篇候选。
- 最多初筛 60 篇。
- 每批 15 篇。
- 最多推荐 10 篇。
- 最多深入分析 3 篇。
- 模型输出 token、超时和重试次数都有硬限制。
- 无新论文时不调用 OpenAI。
- 同一 arXiv 版本不会重复分析。
- 新版本默认只记录，不重新分析。

`models.screening` 和 `models.analysis` 可独立设置。关闭深入分析可将
`limits.max_deep_analysis` 设为 `0`。

## 输出结构

成功运行后可能生成：

```text
content/papers/YYYY-MM-DD.en.md       英文页面
content/papers/YYYY-MM-DD.zh.md       中文页面
static/data/paper-radar/YYYY-MM-DD.json
static/paper-radar.xml
data/processed_papers.json
```

英文页面位于 `/papers/`，中文页面位于 `/zh/papers/`。JSON 会发布到
`/data/paper-radar/YYYY-MM-DD.json`。

在 FreshRSS 中订阅：

```text
https://你的域名/paper-radar.xml
```

自定义域名后，请同步修改 `config/paper-radar.yaml` 中的 `site.base_url`。

## 调整配置

- 增删 arXiv 分类：修改 `arxiv.categories`。
- 修改研究兴趣：编辑 `research_profile.primary_topics` 和
  `research_profile.adjacent_topics`。
- 降低无关方向权重：编辑 `research_profile.low_priority_topics`。
- 修改评分阈值：编辑 `thresholds`。
- 调整每日成本：编辑 `limits`。
- 允许重新分析修订版：将 `versions.analyze_revisions` 设为 `true`。

## 状态与失败处理

`data/processed_papers.json` 记录 base arXiv ID、version、首次发现和处理时间、
发布时间、结果状态、分数、页面路径和内容哈希。排序固定，重复运行不会产生无意义
diff。

网络超时、限流和临时服务错误会有限次数指数退避。某个批次失败时会拆小批次，
尽量保留其他论文结果；鉴权失败或余额不足会让 workflow 明确失败，不会生成空日报。

排查失败时：

1. 打开 GitHub Actions 中失败的 `Daily paper radar` run。
2. 查看失败发生在测试、抓取、分析还是 Hugo 验证步骤。
3. 确认 `OPENAI_API_KEY` Secret 存在且有效。
4. 检查模型名称、余额和 `config/paper-radar.yaml`。
5. 使用 fixture 在本地运行测试，区分代码问题与外部服务问题。

日志只输出数量、批次、失败 ID 和生成文件名，不输出 API Key、授权 Header或完整
模型请求。

## AI 摘要的局限性

第一版不会自动读取 PDF。页面会明确标注所有判断只来自标题和摘要。因此系统不能
验证证明、实验结论、实现可复现性、作者机构或正文中的机制细节；“需要验证的问题”
应作为阅读原文的清单，而不是事实结论。

暂未实现但保留为后续扩展：可选 PDF 全文分析、其他论文源、作者/实验室追踪、
跨日趋势分析和可视化。

## 普通文章与发布

普通英文文章放在 `content/posts/<slug>.en.md`，中文版本放在
`content/posts/<slug>.zh.md`。本地预览：

```bash
docker compose up
```

GitHub 仓库的 **Settings → Pages → Build and deployment → Source** 应设为
**GitHub Actions**。

