# Alvance GitHub Crawler：项目速览与快速上手

## 1. 项目是做什么的

这个项目的目标不是简单地批量抓取 GitHub 仓库，而是自动找到适合做代码任务的开发者库，并把它们加工成可复现、可离线验证的 Harbor/Trace 任务。

一条完整链路是：

```text
GitHub 仓库搜索
    -> 元数据与测试设施初筛
    -> 固定 commit 检出并打分
    -> OpenAI 分析 feature issue，确认待实现方向
    -> GitHub Code Search + grep.app/Sourcegraph 做重复实现核查
    -> E2B 构建仓库环境
    -> 完全断网运行测试，并做三次性能/稳定性基准
    -> 生成 catalog/、materials/、tasks/ 任务包
```

当前支持 Go、Python、TypeScript、JavaScript 和 Rust。最终保存到 Git 的主要是候选记录、拒绝原因、任务描述、环境指纹和 E2B 模板引用；仓库源码、依赖、编译缓存和镜像保存在 E2B 中。

## 2. 核心原理

### 2.1 多道质量门，而不是一次判断

每个仓库需要依次通过硬过滤、软评分、方向检查和运行验证。早期阶段尽量使用便宜的 GitHub API/本地分析，只有少量候选会进入耗时且有费用的 E2B 阶段。

| 阶段 | 主要工作 | 通过条件 | 关键代码 |
| --- | --- | --- | --- |
| Crawl 预抓取 | 按语言搜索并保存断点 | 仓库元数据、活跃度、许可证、精确 head commit 和原生测试证据有效 | `crawl.py` |
| Stage 1 硬过滤 | 做不可妥协的资格检查 | Stars >= 100；最近一年活跃；使用 MIT/Apache-2.0/BSD/ISC/MPL 等宽松许可证；属于支持的语言；有原生测试设施 | `screening/filters.py` |
| Stage 2 检出与软评分 | 检出精确 commit，分析仓库规模和开发者库属性 | 默认总分至少 7/12；默认跳过 GitHub 报告体积超过 100 MB 的仓库 | `workspace.py`、`screening/scoring.py` |
| Stage 3 方向检查 | 读取 feature issue，让模型输出结构化判断 | issue 尚未实现、行为边界清楚、预计至少 200 行、可以客观测试；公开代码搜索不能发现同一实现 | `screening/direction.py` |
| Stage 4 E2B 环境 | 创建或复用 Runtime Template 和 Repository Template | 依赖在构建期安装，仓库按精确 commit 初始化，模板 alias 可复用 | `e2b/template.py`、`runtime/` |
| Stage 5 离线验证 | 在禁止联网的 Sandbox 中运行测试并重复基准 | 测试全部成功；冷启动中位数 < 20 秒；测试中位数 < 120 秒；内存中位数 < 4096 MB | `e2b/offline.py`、`e2b/benchmark.py` |
| Stage 6 打包 | 生成 Trace/Harbor 控制面记录和 wrapper | 写入 catalog、material、task，并记录模板、commit、测试命令和验证收据 | `catalog/`、`pending/registration.py` |

Stage 3 的 H6 核查先调用 GitHub Code Search，再调用 grep.app；grep.app 被拦截或超时时会回退到 Sourcegraph。搜索异常按失败处理，不会把“搜索失败”误判成“没有重复实现”。

Stage 5 默认执行三次。三次测试耗时差至少 15 秒或退出码不一致时，结果会标记为 flaky，并扣 2 分；扣分后仍需达到最低分数，且资源和测试条件都要满足。

### 2.2 精确 commit 是可复现性的基础

候选记录会保存 `base_commit` 和 `source_tree`。后续流程不会只使用仓库当前分支的最新代码，而是重新取得并校验这个 commit。这样可以保证：

- 方向判断、测试和最终任务对应同一份源代码；
- 任务可以在以后重新构建或修复；
- Harbor/Trace 可以在 `/app` 中执行 `git rev-parse` 并生成 patch。

### 2.3 构建时联网，执行时断网

E2B 模板构建阶段允许下载依赖和编译；模板准备好以后，Stage 4/5 创建 Sandbox 时使用 `allow_internet_access=False`。这能发现测试或候选实现是否偷偷依赖运行时网络。

`--skip-e2b` 使用本地 Docker 做离线验证，结果状态是 `offline_verified_local`，只能用于快速本地检查，不等同于最终的 E2B 验证。`--defer-e2b` 则把通过预筛的候选写入 pending 队列，稍后由 E2B worker 消费。

### 2.4 追加式状态与可恢复并发

候选、拒绝和 pending 都采用 JSONL/事件追加方式记录，已有仓库和已完成事件会被识别，程序中断后可以继续。生产模式把 crawl、prescreen 和 E2B verify 拆成并行阶段：pending 达到高水位时暂停上游，降到低水位后继续，避免内存、磁盘或 E2B worker 无限堆积。

编号配置的每个 E2B Key 最多提供 20 个并发槽，因此总并发约等于“已配置 Key 数量 × `PIPELINE_E2B_CONCURRENCY`”。生产环境还会限制本地 checkout 的总磁盘配额，默认不使用容量很小的 `/tmp`。

## 3. 目录和代码地图

| 路径 | 用途 |
| --- | --- |
| `src/alvance_github_crawler/cli.py` | CLI 参数、doctor、crawl/produce/pending 等入口 |
| `src/alvance_github_crawler/config.py` | `.env` 和环境变量解析、默认配置、凭据池 |
| `src/alvance_github_crawler/crawl.py` | GitHub 多语言搜索、初筛、断点和 crawl JSONL |
| `src/alvance_github_crawler/pipeline.py` | 逐仓库串起各阶段；也是最重要的流程阅读入口 |
| `src/alvance_github_crawler/screening/` | 硬过滤、软评分、feature issue/重复实现方向检查 |
| `src/alvance_github_crawler/workspace.py` | 精确 commit 的浅克隆、临时工作区和磁盘配额 |
| `src/alvance_github_crawler/e2b/` | E2B 模板、断网测试、基准和错误分类 |
| `src/alvance_github_crawler/pending/` | 延迟队列、并发消费、失败重试和注册 |
| `src/alvance_github_crawler/catalog/` | material/task/catalog 和 Harbor wrapper 打包 |
| `monitor.py`、`run.sh` | 生产管线启动、恢复和 Rich 终端监控 |
| `tests/` | 不依赖真实 GitHub/OpenAI/Docker/E2B 的单元测试 |
| `docs/` | 运行手册、生产记录和故障分析 |

## 4. 最快上手：先跑通一条小链路

### 4.1 安装依赖并准备配置

要求 Linux/bash、Python 3.11+、Git 和 `uv`。完整 E2B 流程还需要 E2B SDK 和凭据；本地 fallback 需要 Docker daemon。

```bash
uv sync --extra e2b --extra dev
cp .env.example .env
```

编辑 `.env`，至少按计划填写：

- `GITHUB_TOKEN` 或 `GITHUB_TOKEN1`/`GITHUB_TOKEN2`：GitHub 搜索、仓库读取和 Code Search；
- `OPENAI_API_KEY`：Stage 3 的结构化方向判断；
- 完整 E2B 流程再填写 `E2B_API_KEY`，生产量产推荐填写 `E2B_API_KEY1`、`E2B_API_KEY2`、`E2B_API_KEY3`。

不要把真实 Key 写入 Markdown、命令行历史或 Git。`.env` 已被忽略。

### 4.2 先做本机检查

```bash
uv run alvance-github-crawler --doctor
uv run pytest
```

`--doctor` 只显示凭据是否存在、工具和 SDK 是否安装，不会打印 Key 内容。单元测试不会访问真实 API，也不会产生 E2B/Docker 费用。

### 4.3 推荐的三种试跑方式

先用 `--max-repos 1` 验证流程。一个仓库在筛选阶段被拒绝是正常结果，不代表程序失败。

只跑到预筛并放入 pending，不消耗 E2B：

```bash
uv run alvance-github-crawler \
  --defer-e2b --max-repos 1 --verbose
```

有 E2B Key 时跑完整链路，并把并发降到 1 便于观察日志：

```bash
uv run alvance-github-crawler \
  --max-repos 1 --e2b-concurrency 1 --verbose
```

暂时没有 E2B、但本机 Docker daemon 可用时：

```bash
uv run alvance-github-crawler \
  --skip-e2b --max-repos 1 --verbose
```

### 4.4 分阶段运行，便于调试

需要查看 crawl 和 produce 的中间结果时，可以拆开运行：

```bash
uv run alvance-github-crawler crawl \
  --target-total 5 \
  --per-language 1 \
  --output outputs/github_crawl_5

PIPELINE_OUTPUT_DIR=outputs/github_production_5 \
uv run alvance-github-crawler produce \
  --input outputs/github_crawl_5/accepted_repositories.jsonl \
  --defer-e2b --prescreen-concurrency 1 --verbose

PIPELINE_OUTPUT_DIR=outputs/github_production_5 \
uv run alvance-github-crawler \
  --verify-pending --max-repos 1 --e2b-concurrency 1 --verbose
```

`crawl` 会生成 `raw_repositories.jsonl`、`accepted_repositories.jsonl`、`rejected_repositories.jsonl`、`summary.json` 和断点状态。`produce` 会生成或追加 `candidates.jsonl`、`rejections.jsonl`、`pending.jsonl`。

## 5. 生产任务怎么启动

连续量产约定在 `XBY` 分支运行，并使用编号 E2B Key：

```bash
git switch XBY
git pull --ff-only origin XBY
./run.sh
```

`run.sh` 实际启动 `monitor.py`；监控器再启动 `scripts/run_continuous_production.sh`，负责 crawl、prescreen、E2B follower、重试、统计和本地 checkpoint。默认每个 E2B Key 20 并发，prescreen 20 并发；可以通过 `MAX_PER_LANGUAGE`、`BATCH_PER_LANGUAGE`、`PRESCREEN_CONCURRENCY` 和 `E2B_CONCURRENCY` 调整。

生产脚本会在本地提交任务和运行报告，但明确不会自动 `git push`。检查结果后手动推送：

```bash
git push origin XBY
```

运行日志和报告位于 `outputs/production-runs/<run-id>/`；生产状态通常位于 `outputs/github_crawl_500_unquota/` 和 `outputs/github_production_500_unquota/`。出现中断时优先复用同一个 `PIPELINE_RUN_ID` 和已有输出目录恢复。

## 6. 开发一个新改动时的工作顺序

1. 先读 `README.md`、本文件和与目标阶段对应的测试；流程问题优先从 `pipeline.py` 开始跟踪。
2. 修改后先跑最相关的测试，例如：

   ```bash
   uv run pytest tests/test_pipeline.py tests/test_scoring.py tests/test_direction.py
   ```

3. 再跑完整测试：

   ```bash
   uv run pytest
   ```

4. 用 `--doctor` 检查运行时依赖；需要真实 API 时从 `--max-repos 1` 开始，并确认输出 JSONL 和日志中的 stage/reason。
5. 提交时只选择本次改动相关文件。`outputs/` 下经常有正在运行或恢复中的日志，不要无意中把它们一起提交。

最常见的调试定位方式是：先看 `rejections.jsonl` 的 `stage` 和 `reason`，再到对应模块和同名测试中复现。`candidates.jsonl` 是通过验证或预筛的仓库记录，`pending.jsonl` 是等待 E2B 消费的事件队列。

## 7. 一句话记忆

这个项目用 GitHub 找候选，用规则和评分缩小范围，用 OpenAI 把 issue 转成可执行方向，用公开代码搜索排除重复实现，再用 E2B 的断网测试证明任务可运行，最后把结果封装为可复用的 Harbor/Trace 任务。
