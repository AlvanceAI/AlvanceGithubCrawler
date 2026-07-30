# Alvance GitHub Crawler

按《仓库收集与检验管线 — 最终方案》实现的 GitHub 仓库候选收集器。主流程包含：

1. GitHub Search 抓取 Go、Python、TypeScript、JavaScript、Rust 候选；
2. Stars、活跃度、许可证和原生测试设施硬过滤；
3. 文件数、Stars、feature issue、公开符号和开发者库偏好评分（满分 12，默认 7 分入围）；
4. OpenAI 结构化输出分析 feature issue，并通过 GitHub Code Search 与 grep.app 执行 H6 核查；
5. 在 e2b 持久化 Runtime Template 与 Repository Template；
6. 从同一个 Repository Template 启动断网 Sandbox 做 H5 检验和三次执行基准；
7. 将爬取状态写入本地忽略的 `.crawler-state/`；
8. 按 Trace 原生约定生成 `catalog/`、`materials/`、`tasks/`，并在 e2b 持久化 Harbor-compatible wrapper template。

## 从新克隆开始安装

量产脚本面向 Linux/bash，需要 `git`、`uv` 和 `jq`。自动提交 Task 时还需要当前用户
拥有仓库 `XBY` 分支的推送权限，并已配置 Git 提交用户名和邮箱。

```bash
git clone git@github.com:AlvanceAI/AlvanceGithubCrawler.git
cd AlvanceGithubCrawler
git switch XBY
git pull --ff-only origin XBY
uv sync --extra e2b --extra dev
cp .env.example .env
```

后续命令通过 `uv run` 使用项目环境，无需手动激活虚拟环境。

打开 `.env`，至少填写下面这些值。不要把真实 Key 写进 README、命令行或提交记录；
`.env` 已被 Git 忽略。

```dotenv
GITHUB_TOKEN=github_pat_replace_me

OPENAI_API_KEY=sk_replace_me
OPENAI_BASE_URL=
OPENAI_MODEL=gpt-5-mini

E2B_API_KEY=
E2B_API_KEY1=e2b_replace_with_first_key
E2B_API_KEY2=e2b_replace_with_second_key

PIPELINE_E2B_CONCURRENCY=20
PIPELINE_PRESCREEN_CONCURRENCY=20
```

字段说明：

- `GITHUB_TOKEN`：GitHub 仓库搜索、内容读取和 code search；
- `OPENAI_API_KEY`：Stage 3 issue 方向判定；
- `OPENAI_MODEL`：可选，默认 `gpt-5-mini`；
- `OPENAI_BASE_URL`：可选，OpenAI 兼容网关地址；
- `E2B_API_KEY1`、`E2B_API_KEY2`：两个独立 E2B 并发池，每个 Key 最多 20；
- `E2B_API_KEY`：只用于单 Key 命令，双 Key 量产时保持为空。

也支持已有环境的别名 `MODEL_API_KEY`、`MODEL_BASE_URL`、`MODEL_NAME`、`E2B_KEY`，
并可通过 `PIPELINE_ENV_FILE=/path/to/.env` 加载外部文件。未设置 `GITHUB_TOKEN` 时，
程序会尝试安全复用当前 `gh auth` 登录态。

环境自检不会输出密钥内容：

```bash
uv run alvance-github-crawler --doctor
```

开始量产前应确认输出至少包含：`github_token: true`、`openai_api_key: true`、
`e2b_api_key_count: 2`、`e2b_total_concurrency: 40` 和 `e2b_sdk: true`。

## 双 Key 并发量产

量产必须在 `XBY` 分支运行。根目录的一键入口会启动完整的 GitHub 抓取、初筛、方向判断、
E2B 离线测试、资源升级重试、Dockerfile/Task 生成、日志统计和分批推送，并同时显示终端
进度页面：

```bash
git switch XBY
git pull --ff-only origin XBY
./run.sh
```

也可以直接运行同一个入口：

```bash
uv run python monitor.py
```

默认预筛并发为 20；`E2B_API_KEY1` 和 `E2B_API_KEY2` 各使用 20 个并发槽，总 E2B
并发最多 40。完成一轮后会继续扩大抓取范围，直到两个 E2B Key 都耗尽、发生不可恢复错误，
或用户按 `Ctrl+C` 安全暂停。断点和完整日志保存在 `outputs/`，生成的 Task、material、
catalog 和统计文档会自动提交并推送到 `XBY`，不会自动修改 `main`。

启动脚本只检查凭据是否存在，不会输出 Key 内容。若当前不在 `XBY`、缺少两个 E2B Key、
缺少 GitHub/OpenAI 凭据或没有安装 E2B SDK，脚本会在消耗额度前停止并给出修复指令。

## 运行

先用少量仓库验证完整链路：

```bash
uv run alvance-github-crawler --max-repos 5 --verbose
```

暂时没有 e2b 凭据时，可显式使用本地 Docker fallback。此模式写入的状态是 `offline_verified_local`，不是最终的 `ready_for_phase1`：

```bash
uv run alvance-github-crawler --max-repos 5 --skip-e2b
```

覆盖默认搜索条件：

```bash
uv run alvance-github-crawler \
  --query 'language:go stars:100..5000 pushed:>2025-07-01' \
  --search-pages 2 \
  --max-repos 20
```

构建器升级后需要精确重跑历史淘汰项时，可添加 `--retry-rejected`。Docker 基础版本会优先从仓库的 `go.mod`、`pyproject.toml`、`package.json engines` 或 `rust-toolchain` 推导。

爬取状态文件是追加写入的。再次执行时，已经进入 `.crawler-state/candidates.jsonl` 的仓库会跳过；语言配额也会从这个文件恢复。失败记录不会永久去重，因此临时 API 或构建错误修复后可以重试。

通过项目会自动生成轻量 Harbor 封装：本地和 GitHub 只保存 TOML、JSON、Dockerfile 指纹以及测试入口，不保存仓库源码、依赖、编译缓存或镜像。完整环境仅存在 e2b。已有候选可迁移：

```bash
uv run alvance-github-crawler --package-existing
```

大量发现时可先把通过前三阶段的候选写入本地忽略的轻量队列，避免一个耗时较长的
E2B 首次构建阻塞后续仓库发现；消费队列时仍会重新下载精确 commit 到临时目录，
并在单项结束后删除：

```bash
uv run alvance-github-crawler --defer-e2b --max-repos 100
uv run alvance-github-crawler --verify-pending --e2b-concurrency 20
```

新建 E2B template 默认使用 1 vCPU、1024 MB；并发默认上限为每个 Key 20。可分别通过
`PIPELINE_E2B_CPU_COUNT`、`PIPELINE_E2B_MEMORY_MB` 和
`PIPELINE_E2B_CONCURRENCY` 调整。两个编号 Key 可提供 40 个总并发槽。已存在且命中
alias 的 template 会直接复用原规格。
语言配额惩罚默认关闭，因此仓库不会因当前语言占比而被淘汰；只有明确设置
`PIPELINE_LANGUAGE_QUOTA_ENABLED=true` 时才启用原方案中的 S5 配额评分。

迁移后可从项目根目录直接复用远端模板：

```bash
export E2B_API_KEY="${E2B_API_KEY:-$E2B_KEY}"
harbor run \
  --path tasks/<task-name> \
  --env e2b \
  --no-force-build \
  --agent nop \
  --disable-verification
```

不要对这种封装使用 `harbor tasks start-env`，因为当前 Harbor 版本的该命令固定强制重建；`harbor run` 默认会命中已经准备好的 e2b alias。

## 关键实现约定

- 采用方案末尾的最终修订：S6 纳入评分，阈值为 7/12。
- Stage 1 的测试设施检测不只看配置文件：Go 要求 `go.mod` 和 `_test.go`；Node 要求
  test script 和 Jest/Vitest/Mocha 等框架；Python 检查 pytest 配置、测试依赖或 `tests/`；
  Rust 检查 Cargo 测试代码、测试 target 或 dev dependencies。
- Stage 4 与方案伪代码一致：依赖在镜像构建期联网获取，随后在完全断网的容器中跑测试，用于排除运行期联网依赖。
- 默认路径不在本机保存仓库镜像：Runtime Template 按语言/版本持久化在 e2b，Repository Template 按仓库/commit/依赖哈希持久化在 e2b；相同 alias 会直接复用，不重新安装或编译。
- Repository Template 在 e2b 内按精确 commit 初始化真实浅 Git 仓库到 `/app`，因此 Trace 可直接执行 `git rev-parse`、保留 rollout commit 并导出二进制 patch。
- 每个通过仓库还会派生一个只做运行时命令适配的 Harbor wrapper Template。wrapper 构建一次后持久化在 e2b；本地三层 Trace 封装通常只占十余 KB。
- Stage 4 和 Stage 5 复用同一个 e2b Repository Template，二者均设置 `allow_internet_access=False`。本地 Docker 只在 `--skip-e2b` 时启用。
- E2B Runtime/Repository Template 的首次构建不设淘汰超时，只记录构建耗时；600 秒限制仅用于断网测试命令。本地 Docker fallback 仍保留自身构建超时。
- Node 的默认测试命令使用 `CI=1 npm test`，同时兼容 jest 和 vitest。
- H6 的任何搜索异常都会记录为 `stage_error`，不会当作“零结果”放行。
- 当 grep.app 返回 Vercel Security Checkpoint 或连接超时时，使用 Sourcegraph 公共代码索引作为第二独立搜索源，并在候选记录的 `h6_sources` 中标注 `sourcegraph_fallback`；两个来源都不可用时仍失败关闭。
- e2b 超资源阈值时，会依据 LLM 返回的 `target_paths` 尝试生成保守的子集测试命令。
- flaky 定义为三次耗时极差至少 15 秒或退出码不一致，按方案扣 2 分；资源仍超限或扣分后低于 7 时排除。
- 为避免明显不可能满足 e2b 启动/测试阈值的超大仓库阻塞下载，默认跳过 GitHub 报告体积超过 100 MB 的仓库；可用 `PIPELINE_MAX_REPO_SIZE_KB` 调整。tarball 本身另有 200 MB/180 秒保护上限。

## 测试

```bash
uv run pytest
```

单元测试不访问 GitHub、OpenAI、Docker 或 e2b。真实端到端执行会产生 API、Docker 构建与 e2b 费用，建议从 `--max-repos 1` 开始。

完整的 500 仓库生产运行使用可恢复脚本：

```bash
PIPELINE_RUN_ID=github-500-20260729 scripts/run_production_pipeline.sh
```

该脚本默认使用滚动 20 并发，保留逐阶段日志和性能统计，并只对明确的资源失败项从
1 CPU / 1024 MB 升级到 2 CPU / 4096 MB。运行和恢复说明见
[`docs/production-pipeline-runbook.md`](docs/production-pipeline-runbook.md)。

## 初步候选抓取

本轮只抓取并筛选五种语言的候选，不调用 LLM、Docker 或 E2B。`target-total`
表示原始 GitHub 样本数；`per-language` 仅控制每条语言查询抽取多少原始结果，
不限制初筛通过数。500 条原始记录都会被检查，通过项全部进入后续管线：

```bash
uv run alvance-github-crawler crawl \
  --target-total 100 \
  --per-language 20 \
  --output outputs/github_crawl_100
```

该模式生成 `raw_repositories.jsonl`、`accepted_repositories.jsonl`、
`rejected_repositories.jsonl`、`summary.json` 以及断点文件；同一输出目录可重复运行并继续
未完成的语言页。
