# Alvance GitHub Crawler

按《仓库收集与检验管线 — 最终方案》实现的 GitHub 仓库候选收集器。主流程包含：

1. GitHub Search 抓取 Go、Python、TypeScript、JavaScript、Rust 候选；
2. Stars、活跃度、许可证和原生测试设施硬过滤；
3. 文件数、Stars、feature issue、公开符号、语言配额、开发者库偏好评分（满分 12，默认 7 分入围）；
4. OpenAI 结构化输出分析 feature issue，并通过 GitHub Code Search 与 grep.app 执行 H6 核查；
5. 在 e2b 持久化 Runtime Template 与 Repository Template；
6. 从同一个 Repository Template 启动断网 Sandbox 做 H5 检验和三次执行基准；
7. 写入 `output/candidates.jsonl`，所有排除原因写入 `output/rejections.jsonl`。

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[e2b,dev]'
cp .env.example .env
```

填写：

- `GITHUB_TOKEN`：GitHub 仓库搜索、内容读取和 code search；
- `OPENAI_API_KEY`：Stage 3 issue 方向判定；
- `OPENAI_MODEL`：可选，默认 `gpt-5-mini`；
- `OPENAI_BASE_URL`：可选，OpenAI 兼容网关地址；
- `E2B_API_KEY`：Stage 5 template 和 benchmark。

也支持已有环境的别名 `MODEL_API_KEY`、`MODEL_BASE_URL`、`MODEL_NAME`、`E2B_KEY`，
并可通过 `PIPELINE_ENV_FILE=/path/to/.env` 加载外部文件。未设置 `GITHUB_TOKEN` 时，
程序会尝试安全复用当前 `gh auth` 登录态。

环境自检不会输出密钥内容：

```bash
alvance-github-crawler --doctor
```

## 运行

先用少量仓库验证完整链路：

```bash
alvance-github-crawler --max-repos 5 --verbose
```

暂时没有 e2b 凭据时，可显式使用本地 Docker fallback。此模式写入的状态是 `offline_verified_local`，不是最终的 `ready_for_phase1`：

```bash
alvance-github-crawler --max-repos 5 --skip-e2b
```

覆盖默认搜索条件：

```bash
alvance-github-crawler \
  --query 'language:go stars:100..5000 pushed:>2025-07-01' \
  --search-pages 2 \
  --max-repos 20
```

构建器升级后需要精确重跑历史淘汰项时，可添加 `--retry-rejected`。Docker 基础版本会优先从仓库的 `go.mod`、`pyproject.toml`、`package.json engines` 或 `rust-toolchain` 推导。

输出文件是追加写入的。再次执行时，已经进入 `candidates.jsonl` 的仓库会跳过；语言配额也会从这个文件恢复。失败记录不会永久去重，因此临时 API 或构建错误修复后可以重试。

## 关键实现约定

- 采用方案末尾的最终修订：S6 纳入评分，阈值为 7/12。
- Stage 1 的测试设施检测不只看文件名：Go 还要求 `_test.go`，Node 检查 jest/vitest，Python 检查 pytest 配置，Rust 检查 `[dev-dependencies]`。
- Stage 4 与方案伪代码一致：依赖在镜像构建期联网获取，随后在完全断网的容器中跑测试，用于排除运行期联网依赖。
- 默认路径不在本机保存仓库镜像：Runtime Template 按语言/版本持久化在 e2b，Repository Template 按仓库/commit/依赖哈希持久化在 e2b；相同 alias 会直接复用，不重新安装或编译。
- Stage 4 和 Stage 5 复用同一个 e2b Repository Template，二者均设置 `allow_internet_access=False`。本地 Docker 只在 `--skip-e2b` 时启用。
- Node 的默认测试命令使用 `CI=1 npm test`，同时兼容 jest 和 vitest。
- H6 的任何搜索异常都会记录为 `stage_error`，不会当作“零结果”放行。
- 当 grep.app 明确返回 Vercel Security Checkpoint 时，使用 Sourcegraph 公共代码索引作为第二独立搜索源，并在候选记录的 `h6_sources` 中标注 `sourcegraph_fallback`；普通搜索错误仍失败关闭。
- e2b 超资源阈值时，会依据 LLM 返回的 `target_paths` 尝试生成保守的子集测试命令。
- flaky 定义为三次耗时极差至少 15 秒或退出码不一致，按方案扣 2 分；资源仍超限或扣分后低于 7 时排除。
- 为避免明显不可能满足 e2b 启动/测试阈值的超大仓库阻塞下载，默认跳过 GitHub 报告体积超过 100 MB 的仓库；可用 `PIPELINE_MAX_REPO_SIZE_KB` 调整。tarball 本身另有 200 MB/180 秒保护上限。

## 测试

```bash
pytest
```

单元测试不访问 GitHub、OpenAI、Docker 或 e2b。真实端到端执行会产生 API、Docker 构建与 e2b 费用，建议从 `--max-repos 1` 开始。
