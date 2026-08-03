# AlvanceGithubCrawler 交付文档

`AlvanceGithubCrawler` 是面向 DeepSWE Bench 生产前置阶段的 GitHub 仓库收集、筛选、环境验证和材料导出工具。它的职责不是直接生成最终 DeepSWE/Harbor 问题包，而是稳定产出可被 `AlvanceDeepSWE` 消费的高质量仓库材料：真实 GitHub 仓库、固定 commit、可运行测试命令、E2B/Harbor 环境信息、方向候选和轻量任务封装。

当前推荐的生产边界：

- Crawler 负责发现、筛选、验证仓库材料，并写出 `catalog/`、`materials/`、`tasks/`、`.crawler-state/` 等控制面产物。
- DeepSWE 负责基于这些材料进一步生成 instruction、verifier、answer、轨迹和最终 Harbor 问题包。
- 生产环境统一使用 conda 环境 `bench`。不要在仓库内创建或依赖 `.venv`，也不要把真实 API key 写入仓库、README、命令行历史或产物。

## 环境安装

在总工作区根目录运行：

```bash
conda activate bench
python -m pip install -e AlvanceGithubCrawler[e2b]
```

如果只做本地单元测试、不调用 E2B，可省略 `[e2b]`：

```bash
conda activate bench
python -m pip install -e AlvanceGithubCrawler
```

### 工作目录约定

除非命令明确写了总工作区路径，本文后续 Crawler 独立命令默认在 Crawler 包根目录执行：

```bash
cd /home/wyy/Workspace/Benchmark/DeepSWE/AlvanceGithubCrawler
```

原因是当前实现中的 `.env`、`.crawler-state`、`catalog`、`materials`、`tasks` 等默认路径都是相对当前工作目录解析的。如果在总工作区根目录直接运行 `alvance-github-crawler`，这些目录会被写到总根目录，容易与 DeepSWE 的产物混在一起。

如果确实需要从其他目录运行，必须显式设置：

```bash
export PIPELINE_ENV_FILE=/home/wyy/Workspace/Benchmark/DeepSWE/AlvanceGithubCrawler/.env
export PIPELINE_OUTPUT_DIR=/home/wyy/Workspace/Benchmark/DeepSWE/AlvanceGithubCrawler/.crawler-state
export PIPELINE_CATALOG_DIR=/home/wyy/Workspace/Benchmark/DeepSWE/AlvanceGithubCrawler/catalog
```

生产前自检：

```bash
conda run --no-capture-output -n bench alvance-github-crawler --doctor
```

自检只输出布尔值、计数和模型名，不应输出密钥内容。正式生产至少应看到：

- `github_token: true` 或 `github_token_count > 0`
- `openai_api_key: true`
- `e2b_api_key_count > 0`
- `git: true`
- `openai_sdk: true`
- `e2b_sdk: true`

`docker: false` 不一定阻塞 E2B 生产；只有显式走本地 Docker fallback 时才需要本机 Docker。

## 凭据与配置

Crawler 当前没有 TOML profile；配置主要来自环境变量、`.env` 和 CLI 参数。

### 配置文件位置

默认会读取当前工作目录下的：

```text
.env
```

按本文工作目录约定执行时，它就是 `AlvanceGithubCrawler/.env`。

也可通过外部路径覆盖：

```bash
export PIPELINE_ENV_FILE=/path/to/crawler.env
```

配置优先级：

```text
进程环境变量 > PIPELINE_ENV_FILE 指向的 dotenv > 当前工作目录 .env > 代码默认值
```

注意：进程环境优先级最高。如果 shell 里已经 export 了某个变量，`.env` 中同名字段不会覆盖它。

### 凭据字段

```dotenv
GITHUB_TOKEN=
GITHUB_TOKEN1=
GITHUB_TOKEN2=

OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_MODEL=gpt-5-mini

E2B_API_KEY=
E2B_API_KEY1=
E2B_API_KEY2=
E2B_API_KEY3=
```

字段语义：

- `GITHUB_TOKEN1`、`GITHUB_TOKEN2`：GitHub API token 池，按编号顺序去重轮询。用于仓库搜索、文件读取、tree、issue 和 code search。
- `GITHUB_TOKEN`：单 token 回退。没有编号 token 时使用。
- `OPENAI_API_KEY`：方向判断阶段使用的 OpenAI 兼容模型凭据。
- `OPENAI_BASE_URL`：OpenAI 兼容网关地址。若只给域名根路径，代码会补 `/v1`。
- `OPENAI_MODEL`：方向判断模型，默认 `gpt-5-mini`。
- `E2B_API_KEY1`、`E2B_API_KEY2`、`E2B_API_KEY3`：E2B key 池，按编号顺序去重轮询。
- `E2B_API_KEY`：单 key 回退。没有编号 key 时使用。

兼容别名：

- `MODEL_API_KEY` 等同于 `OPENAI_API_KEY`
- `MODEL_BASE_URL` 等同于 `OPENAI_BASE_URL`
- `MODEL_NAME` 等同于 `OPENAI_MODEL`
- `E2B_KEY` 等同于 `E2B_API_KEY`

如果没有配置 GitHub token，程序会尝试使用本机 `gh auth token` 的登录态，但生产不建议依赖隐式凭据。

### 生产参数环境变量

这些变量由 `PipelineConfig.from_env()` 读取：

- `PIPELINE_OUTPUT_DIR`：Crawler 状态目录，默认 `.crawler-state`。
- `PIPELINE_CATALOG_DIR`：Trace/Harbor 控制面 catalog 目录，默认 `catalog`。
- `PIPELINE_FEATURE_ISSUE_LIMIT`：Stage 3 检查 feature issue 的数量上限，默认 `10`。
- `PIPELINE_OPENAI_TIMEOUT_S`：方向判断 LLM 请求超时，默认 `120`。
- `PIPELINE_OPENAI_MAX_OUTPUT_TOKENS`：方向判断输出 token 上限，默认 `1000`。
- `PIPELINE_E2B_CPU_COUNT`：E2B template CPU，默认 `1`。
- `PIPELINE_E2B_MEMORY_MB`：E2B template 内存，默认 `1024`。
- `PIPELINE_E2B_CONCURRENCY`：每个 E2B key 的并发，默认 `20`，必须在 `1..20`。
- `PIPELINE_PRESCREEN_CONCURRENCY`：仓库 checkout、评分和方向判断并发，默认 `1`，必须在 `1..20`。
- `PIPELINE_LANGUAGE_QUOTA_ENABLED`：是否启用语言占比惩罚，默认 `false`。
- `PIPELINE_MAX_REPO_SIZE_KB`：GitHub 报告仓库大小上限，默认 `100000`。

代码内仍有一些固定默认值：

- 支持语言：`go`、`python`、`typescript`、`javascript`、`rust`。
- 软评分入围阈值：`min_soft_score = 7.0`。
- GitHub 搜索每页候选数：`max_candidates_per_query = 100`。
- 默认搜索页数：`search_pages = 1`，可由 CLI `--search-pages` 覆盖。
- E2B 离线测试命令超时：`build_timeout_s = 600`。
- E2B benchmark 单次命令超时：`benchmark_timeout_s = 600`。
- benchmark 次数：`benchmark_runs = 3`。
- tree summary 限制：`max_tree_entries = 1500`，`max_tree_chars = 18000`。

这些固定值如果后续需要大规模调参，建议优先迁移为环境变量或 profile 文件，不要在流程代码里继续散落魔法数字。

## 常用命令

### 环境自检

```bash
conda run --no-capture-output -n bench alvance-github-crawler --doctor
```

### 少量仓库完整试跑

实时搜索 GitHub，并对最多 5 个新仓库跑完整 pipeline：

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --max-repos 5 \
  --verbose
```

### 只抓取初筛候选

不调用 LLM、Docker 或 E2B，只写 crawl 输出：

```bash
conda run --no-capture-output -n bench alvance-github-crawler crawl \
  --target-total 100 \
  --per-language 20 \
  --output outputs/github_crawl_100 \
  --verbose
```

`--target-total` 必须等于 `--per-language * 5`，因为当前固定抓取五种语言。

输出目录包含：

- `raw_repositories.jsonl`
- `accepted_repositories.jsonl`
- `rejected_repositories.jsonl`
- `summary.json`
- checkpoint 文件

### 基于 crawl 结果生产候选

```bash
conda run --no-capture-output -n bench alvance-github-crawler produce \
  --input outputs/github_crawl_100/accepted_repositories.jsonl \
  --max-repos 10 \
  --verbose
```

只生产指定仓库，可重复 `--repository`：

```bash
conda run --no-capture-output -n bench alvance-github-crawler produce \
  --input outputs/github_crawl_100/accepted_repositories.jsonl \
  --repository owner/repo-a \
  --repository owner/repo-b \
  --verbose
```

### 分离 prescreen 与 E2B 验证

先把通过初筛和方向判断的候选放入 pending 队列：

```bash
conda run --no-capture-output -n bench alvance-github-crawler produce \
  --input outputs/github_crawl_100/accepted_repositories.jsonl \
  --defer-e2b \
  --prescreen-concurrency 8 \
  --verbose
```

再消费 pending 队列执行 E2B template、断网测试、benchmark 和 Harbor wrapper 包装：

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --verify-pending \
  --e2b-concurrency 4 \
  --verbose
```

这种方式更适合大规模生产，因为长尾 E2B 构建不会阻塞前面的 GitHub 发现和方向判断。

### 本地 fallback

没有 E2B 凭据时可跳过 E2B：

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --max-repos 5 \
  --skip-e2b \
  --verbose
```

该模式会写入 `offline_verified_local`，不能等价视为最终可用于 DeepSWE 的 E2B 材料。

### 重新打开失败项

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --requeue-failures \
  --failure-reason e2b_resource_exhausted \
  --failure-reason benchmark_resource_fail \
  --verbose
```

可加 `--failure-contains TEXT` 进一步限制错误日志包含某段文本的失败项。

### 打包已有 qualified 候选

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --package-existing \
  --verbose
```

用于已有 `.crawler-state/candidates.jsonl` 或 `catalog/e2b-packages.jsonl`，但还需要补齐 Harbor/E2B wrapper 的场景。

### 导出 DeepSWE handoff

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --export-deepswe-input \
  --repo owner/repo \
  --out outputs/owner-repo-handoff.json
```

该 JSON 是 DeepSWE 消费 Crawler 结果的桥接输入。

### 导出 repo summary

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --export-repo-summary \
  --repo owner/repo \
  --out outputs/owner-repo.summary.json
```

用于 DeepSWE 生成 repo card 或做材料 review。

### 导出 Material 目录

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --export-materials \
  --repo-count 5 \
  --material-dir Material \
  --clone-repos \
  --require-clone \
  --clone-timeout-s 120
```

该命令从本地 Crawler 产物选择可用记录，准备 DeepSWE/Harbor 材料目录。`--clone-repos` 会把仓库 clone 到 Material 内；不加时只导出元数据和已有材料。

### 多样性报告

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --diversity-report \
  --out catalog/diversity-report.md
```

报告按语言、领域、质量和 DeepSWE feedback 汇总候选分布，用于批量生产时避免样本过度集中。

### 记录 DeepSWE 反馈

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --record-deepswe-feedback \
  --repo owner/repo \
  --base-commit 0123456789abcdef0123456789abcdef01234567 \
  --material-id example-material \
  --task-id example-task \
  --outcome abandoned \
  --reason verifier_weak \
  --notes "verifier could not distinguish API-compatible failure"
```

反馈默认写入 `catalog/deepswe-feedback.jsonl`，也可用 `--out` 指定路径。

### 查看生产事件

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --events \
  --tail 50
```

筛选某个仓库：

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --events \
  --repo owner/repo \
  --tail 20
```

## CLI 参数语义

`alvance-github-crawler` 有两类用法：

- 子命令模式：`crawl` 和 `produce`。
- 直接模式：不写子命令时，直接从 GitHub 搜索并运行完整 pipeline。

### 通用参数

- `--query QUERY`：覆盖默认 GitHub search query，可重复。
- `--max-repos N`：最多处理多少个新仓库。
- `--search-pages N`：实时搜索模式下每条 query 抓取多少页，必须大于等于 1。
- `--prescreen-concurrency N`：checkout、软评分、方向判断并发，范围 `1..20`。
- `--e2b-concurrency N`：每个 E2B key 的并发，范围 `1..20`。
- `--skip-e2b`：跳过 E2B，用本地 Docker fallback 或只注册本地验证结果。
- `--defer-e2b`：prescreen 通过后写 pending 队列，不立即跑 E2B。
- `--verify-pending`：消费 pending 队列。
- `--requeue-failures`：把指定失败原因重新放回 pending。
- `--failure-reason REASON`：`--requeue-failures` 使用的失败原因，可重复。
- `--failure-contains TEXT`：按错误文本进一步过滤失败项。
- `--retry-rejected`：实时 pipeline 中允许重新尝试历史 terminal rejection。
- `--verbose`：输出更详细日志。
- `--doctor`：环境与凭据自检。

### `crawl` 参数

- `--target-total N`：总原始样本数，必须等于 `--per-language * 5`。
- `--per-language N`：每种语言抓取多少条原始记录。
- `--output DIR`：crawl 输出目录。
- `--max-search-pages N`：每种语言最多请求多少 GitHub Search 页，GitHub Search API 上限通常为 10。
- `--request-interval SECONDS`：GitHub 请求最小间隔。
- `--api-timeout SECONDS`：GitHub 请求超时。

### `produce` 参数

- `--input PATH`：消费 `accepted_repositories.jsonl`。
- `--repository OWNER/REPO`：只生产指定仓库，可重复且保持顺序。
- `--max-repos N`：从输入里最多选择多少个未处理仓库。
- `--defer-e2b`：只做 prescreen 并入队。
- `--skip-e2b`：不使用 E2B，写本地验证结果。

### 导出与辅助参数

- `--package-existing`：为已有候选补 Harbor/E2B wrapper。
- `--export-deepswe-input`：导出单个候选的 DeepSWE handoff JSON，要求 `--repo` 和 `--out`。
- `--export-repo-summary`：导出单个候选的 summary JSON，要求 `--repo` 和 `--out`。
- `--diversity-report`：写多样性报告，默认输出到 `catalog/diversity-report.md`。
- `--record-deepswe-feedback`：追加 DeepSWE 生产反馈，要求 `--repo`、`--base-commit`、`--outcome`、`--reason`。
- `--task-id`、`--material-id`、`--base-commit`、`--outcome`、`--reason`、`--notes`：feedback 模式字段。
- `--events`：打印 `.crawler-state/events.jsonl`。
- `--tail N`：事件输出只保留最后 N 行。
- `--export-materials`：导出 DeepSWE Material 目录。
- `--repo-count N`：`--export-materials` 选择仓库数，默认 5。
- `--material-dir DIR`：`--export-materials` 输出目录，默认 `Material`。
- `--clone-repos`：导出材料时 clone 仓库。
- `--require-clone`：clone 失败即失败。
- `--clone-timeout-s N`：clone 相关单命令超时，默认 120 秒。

## 执行流程

### 1. GitHub crawl

目标：

- 从五种语言按 query 抓取原始仓库记录。
- 固定 repo、默认分支、base commit、source tree、stars、license、topics、pushed_at、测试证据等快照字段。
- 生成可恢复的 crawl 输出，后续 produce 不应随 GitHub 默认分支漂移而改变材料语义。

主要产物：

- `outputs/<crawl-run>/raw_repositories.jsonl`
- `outputs/<crawl-run>/accepted_repositories.jsonl`
- `outputs/<crawl-run>/rejected_repositories.jsonl`
- `outputs/<crawl-run>/summary.json`

### 2. Stage 1 hard filter

目标是先剔除明显不适合 DeepSWE 的仓库。当前硬过滤包括：

- stars 至少 100。
- 最近一年有 push。
- 许可证在许可列表内：MIT、Apache-2.0、BSD-2-Clause、BSD-3-Clause、ISC、MPL-2.0。
- 语言属于 Go、Python、TypeScript、JavaScript、Rust。
- 存在原生测试设施。

测试设施不是简单看目录名：

- Go：需要 `go.mod` 和 `_test.go`。
- Python：检查 `tests/`、pytest 配置、`conftest.py` 或 requirements 中 pytest。
- Node：需要 `package.json` test script，并能识别 Jest、Vitest、Mocha、Node test、Bun test 等。
- Rust：检查 `Cargo.toml`、integration tests、test target 或 dev dependencies。

失败会写入 `.crawler-state/rejections.jsonl`，stage 通常为 `stage1_hard_filter`。

### 3. Stage 2 checkout and soft score

目标：

- clone 精确 commit。
- 用本地 tree summary、文件数量、public symbol、stars、feature issue、开发者库信号等计算软评分。
- 过滤明显过小、过大、缺少公共 API 或不适合构造成库级任务的项目。

当前软评分满分 12：

- `S1_file_count`：文件数规模。
- `S2_stars`：star 区间。
- `S3_feature_issues`：是否存在 feature issue。
- `S4_public_symbols`：公共符号数量。
- `S5_language_quota`：语言配额项，默认不强制语言占比时通常为通过。
- `S6_developer_lib`：是否具有 library/sdk/framework/parser/client/driver 等开发者库信号。

默认入围阈值为 `7.0`。

### 4. Stage 3 direction

目标：

- 让 OpenAI 兼容模型基于 issue、仓库摘要和 tree summary 判断是否存在适合 DeepSWE 的功能扩展方向。
- 生成方向描述、关键词、目标路径候选。
- 用 GitHub Code Search、grep.app 或 Sourcegraph fallback 做公开实现核查，避免选择已有明显公开实现污染的问题。

结果会进入候选记录的 `direction`、`direction_keywords`、`direction_target_paths`、`h6_sources`。

### 5. Stage 3.5 E2B environment

目标：

- 基于语言和依赖推导 runtime。
- 在 E2B 中构建 Runtime Template 和 Repository Template。
- Repository Template 固定精确 commit，并在 `/app` 保留真实 Git 仓库。

E2B template alias 会进入 `catalog/e2b-packages.jsonl`、`materials/<material-id>/material.toml` 和 receipt，供 DeepSWE/Harbor 后续复用。

### 6. Stage 4 offline test

目标：

- 从同一个 E2B Repository Template 启动断网 sandbox。
- 执行原生测试命令，确认仓库不依赖运行期联网。

失败原因可能包括：

- `offline_test_timeout`
- `benchmark_test_fail`
- `e2b_resource_exhausted`
- `build_fail`
- `infra_error`

### 7. Stage 5 benchmark

目标：

- 重复运行测试命令，默认 3 次。
- 记录 cold start、中位测试耗时、峰值内存、exit code 稳定性。
- 判断是否 flaky、是否资源超限。

flaky 会扣 2 分；若扣分后低于软评分阈值，会被拒绝。

### 8. Stage 6 Harbor package

目标：

- 为通过 E2B 验证的仓库生成 Harbor-compatible wrapper。
- 写入 Trace 风格三层控制面：`catalog/`、`materials/`、`tasks/`。
- 通过 `harbor run --env e2b --no-force-build` 复用已有 E2B alias。

Crawler 生成的 task 是材料级方向任务，不是最终 DeepSWE Bench 问题包。最终 instruction、verifier 和轨迹仍由 DeepSWE 管线生成。

## 产物结构

### `.crawler-state/`

默认状态目录，可通过 `PIPELINE_OUTPUT_DIR` 改变：

```text
.crawler-state/
├── candidates.jsonl
├── rejections.jsonl
├── pending.jsonl
└── events.jsonl
```

- `candidates.jsonl`：成功注册或已验证候选，按 JSONL 追加。包含 repo、base commit、score、direction、environment、benchmark、harbor package 等信息。
- `rejections.jsonl`：被拒绝或阶段异常的候选，包含 stage、reason、错误摘要和相关证据。
- `pending.jsonl`：`--defer-e2b` 生成的待验证队列。
- `events.jsonl`：生产事件流，可用 `--events` 查看。

### `catalog/`

```text
catalog/
├── e2b-packages.jsonl
├── repo-materials.toml
├── diversity-report.md
└── deepswe-feedback.jsonl
```

- `e2b-packages.jsonl`：qualified package 总账，含 E2B alias、Harbor wrapper、测试命令、资源、benchmark 和材料路径。
- `repo-materials.toml`：Trace 风格 material 索引。
- `diversity-report.md`：候选多样性报告。
- `deepswe-feedback.jsonl`：DeepSWE 后续生产结果反馈。

### `materials/<material-id>/`

典型内容：

```text
materials/<material-id>/
├── README.md
├── material.toml
├── environment/Dockerfile
├── receipts/e2b.json
└── ...
```

`material.toml` 保存 repo、commit、source tree、语言、runtime、E2B template、测试命令和 Harbor 环境信息。材料目录不应包含 API key、私有 token、完整源码镜像、依赖缓存或本机临时路径。

### `tasks/<task-id>/`

典型内容：

```text
tasks/<task-id>/
├── task.toml
├── material.toml
├── direction.md
├── instruction.md
├── environment/Dockerfile
├── tests/test.sh
└── solution/solve.sh
```

该 task 是 Crawler 阶段的 Harbor-compatible material wrapper，用于确认环境可启动和测试命令可运行。不要把它误解为最终隐藏 verifier 完备的 DeepSWE 题目包。

### `outputs/production-runs/<RUN_ID>/`

历史批处理脚本会生成：

```text
outputs/production-runs/<RUN_ID>/
├── crawl/
├── production/
├── logs/
├── stage-timings.jsonl
├── metrics.json
└── statistics.md
```

其中 `metrics.json` 和 `statistics.md` 用于写生产统计；`logs/` 保留每个阶段 stdout/stderr。

## 如何分析运行结果

### 快速判断本轮是否成功

1. 看命令最终 JSON summary。
2. 看 `.crawler-state/events.jsonl` 是否有持续新增。
3. 看 `.crawler-state/candidates.jsonl` 中是否有新增 `ready_for_phase1` 或 `qualified` 记录。
4. 看 `.crawler-state/rejections.jsonl` 的 `stage` 和 `reason` 是否集中在某一类。

### 常见状态含义

- `registered`：候选已注册。
- `queued`：prescreen 通过，已进入 pending，尚未跑 E2B。
- `duplicate`：该 repo 已在 candidate、pending 或 catalog 中存在。
- `rejected`：质量或环境原因拒绝。
- `error`：阶段异常，通常需要看 `error_type` 和日志。
- `key_exhausted`：E2B key 额度或并发槽耗尽。
- `offline_verified_local`：本地 fallback 通过，但不是最终 E2B qualified。
- `ready_for_phase1`：E2B 离线测试和 benchmark 通过，可供 DeepSWE 使用。
- `ready_for_phase1_flaky_test_suite`：测试可用但存在 flaky 扣分风险。

### 常见 rejection stage

- `stage1_hard_filter`：stars、活跃度、许可证、语言或测试设施不满足。
- `stage2_checkout`：clone 或 checkout 失败。
- `stage2_soft_score`：软评分不足或仓库过大。
- `stage3_direction`：没有合适功能扩展方向，或公开实现污染风险无法排除。
- `stage3_5_e2b_environment`：E2B runtime/repository template 构建失败。
- `stage4_e2b_offline_test`：断网测试失败。
- `stage5_e2b_benchmark`：benchmark 不稳定、资源超限或测试失败。
- `stage6_harbor_package`：Harbor wrapper 包装失败。

### 调试命令

查看最近事件：

```bash
conda run --no-capture-output -n bench alvance-github-crawler --events --tail 50
```

查看某个 repo：

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --events \
  --repo owner/repo \
  --tail 50
```

统计 rejection 分布：

```bash
python - <<'PY'
import json
from collections import Counter
from pathlib import Path

path = Path("AlvanceGithubCrawler/.crawler-state/rejections.jsonl")
counts = Counter()
for line in path.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    item = json.loads(line)
    counts[(item.get("stage"), item.get("reason"))] += 1
for (stage, reason), count in counts.most_common(30):
    print(count, stage, reason)
PY
```

## 与 DeepSWE 管线的衔接

DeepSWE 可以通过三种方式消费 Crawler 结果：

1. 直接指定 Crawler task：

```bash
conda run --no-capture-output -n bench alvance-produce-sweharbor \
  --root AlvanceDeepSWE \
  --crawler-root AlvanceGithubCrawler \
  --crawler-task alv-example-task-v2 \
  --api-key-file /home/wyy/Workspace/Benchmark/DeepSWE/api_key.json \
  --require-harbor-cli \
  --require-e2b-cli \
  --verbose
```

2. 批量扫描 Crawler qualified 任务：

```bash
conda run --no-capture-output -n bench alvance-produce-sweharbor \
  --root AlvanceDeepSWE \
  --crawler-root AlvanceGithubCrawler \
  --all \
  --repo-count 3 \
  --samples-per-repo 2 \
  --api-key-file /home/wyy/Workspace/Benchmark/DeepSWE/api_key.json \
  --require-harbor-cli \
  --require-e2b-cli \
  --continue-on-error \
  --out analysis/three-repos-two-each-summary.json \
  --report-out analysis/production-reports \
  --feedback-out analysis/crawler-feedback.jsonl \
  --jsonl-events analysis/three-repos-two-each-events.jsonl \
  --explain-next \
  --verbose
```

3. 先导出 handoff 或 Material，再由 DeepSWE 显式消费：

```bash
conda run --no-capture-output -n bench alvance-github-crawler \
  --export-deepswe-input \
  --repo owner/repo \
  --out outputs/owner-repo-handoff.json
```

DeepSWE 侧如果最终 abandon 某个材料，应回写 feedback，避免 Crawler 后续继续优先选择同类问题。

## 历史脚本与当前生产标准

仓库保留了这些历史脚本：

- `run.sh`
- `monitor.py`
- `scripts/run_production_pipeline.sh`
- `scripts/run_continuous_production.sh`

它们用于早期 XBY 分支连续量产，内部仍可能调用 `uv run`，并带有自动提交、推送、压缩 raw crawl 等行为。当前统一 bench 环境下，推荐优先使用 `conda run -n bench alvance-github-crawler ...` 和 DeepSWE 的 `alvance-produce-sweharbor ...` 组合。

如果必须使用历史脚本，需要先审查：

- 是否会自动 `git add/commit/push`。
- 是否仍依赖 `uv`。
- 输出目录是否会覆盖当前实验。
- `PIPELINE_RUN_ID`、`PIPELINE_RUN_ROOT` 是否唯一。
- 是否会把 raw API payload 或本地路径加入 Git。

## 质量标准与蚂蚁需求对应

Crawler 对 DeepSWE Bench 的贡献主要体现在材料质量：

- 真实仓库：仓库来自 GitHub，记录 repo URL、base commit 和 source tree。
- 可复现环境：通过 E2B Repository Template、断网测试和 benchmark 验证。
- 可运行测试：每个候选必须有原生测试设施和测试命令。
- 低污染风险：Stage 3 使用公开实现搜索，发现明显已有实现时拒绝。
- 可追溯：候选、拒绝、pending、events、catalog、material、task 都是结构化产物。
- 可批量恢复：crawl、pending、candidate registry 和 production run 输出都支持断点续跑。

Crawler 不能替代 DeepSWE 的隐藏 verifier 校准。它只能证明“这个仓库材料适合生成问题”，不能证明“最终问题包具备合理难度、隐藏 verifier 充分、轨迹分布健康”。

## 当前不足和风险点

### 1. 配置方式仍偏环境变量

Crawler 当前没有类似 DeepSWE 的 TOML profile。环境变量适合脚本，但不利于记录一次实验的完整配置快照。后续如果继续扩展，建议引入显式 profile 文件，并在 summary 中写出实际生效配置。

### 2. 历史脚本仍含 `uv run`

生产统一到 conda `bench` 后，历史脚本如果直接使用可能绕过 bench 环境。建议优先走 console script；若继续保留脚本，应逐步改为可配置 Python 入口或显式 `conda run -n bench`。

### 3. 自动提交/推送有污染风险

持续量产脚本可能自动提交 `catalog`、`materials`、`tasks` 和统计文档。正式运行前必须确认 `.gitignore`、输出目录和 raw payload 处理策略，避免提交本机路径、密钥、临时日志或大体积产物。

### 4. 网关和 GitHub/E2B 额度影响明显

GitHub rate limit、OpenAI 兼容网关超时、E2B key 额度耗尽都会造成大规模生产中断。需要使用 `--defer-e2b`、pending 队列、分 key 并发和 events/rejections 报告区分“材料质量失败”和“基础设施失败”。

### 5. 方向判断仍依赖 LLM

Stage 3 的 direction quality 会影响 DeepSWE 后续成包率。方向过浅、API contract 不清、目标路径过散，都可能导致 DeepSWE Roll 1/2 大量 revise 或 reject。应持续利用 `deepswe-feedback.jsonl` 反哺 Crawler 排序。

### 6. Crawler task 不是最终题包

`tasks/<task-id>` 只是材料 wrapper 和方向载体。最终交付前必须经过 DeepSWE 的 instruction lock、verifier lock、answer lock、trajectory report、package manifest 和 runtime validation。

## 开发与测试

单元测试：

```bash
conda run --no-capture-output -n bench pytest AlvanceGithubCrawler/tests
```

代码风格：

```bash
conda run --no-capture-output -n bench ruff check AlvanceGithubCrawler/src AlvanceGithubCrawler/tests
```

单元测试不应访问 GitHub、OpenAI、Docker 或 E2B。真实端到端测试会消耗 API 和 E2B 额度，应从 `--max-repos 1` 或小 crawl 目录开始。

## 文档维护原则

后续修改 Crawler 代码时，需要同步更新本 README，尤其是：

- 新增或删除 CLI 参数。
- 新增环境变量或改变默认值。
- 调整筛选、评分、E2B、benchmark 或 Harbor 包装逻辑。
- 改变 `.crawler-state`、`catalog`、`materials`、`tasks` 的结构。
- 改变与 DeepSWE 的 handoff、feedback 或 Material 导出格式。

文档应保持“生产可执行、参数可追溯、风险可排查”的结构，不要堆积历史流水账。
