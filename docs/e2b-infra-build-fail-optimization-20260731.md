# E2B `infra_error` / `build_fail` 优化调研简报

> 调研数据快照：`2026-07-31 04:30 UTC`。修复于 `2026-07-31` 完成，生产管线保持暂停，尚未消耗 E2B 额度验证真实通过率。

## 修复状态

已完成以下 P0 修复：

- Node 按 npm、pnpm、Yarn v1/Yarn Berry 的 lockfile 选择确定性安装命令；没有受支持 lockfile 的项目明确标记为 `unsupported_dependency_lock`。
- Go 1.22 及以下使用镜像内置 Go 1.22 和 `GOTOOLCHAIN=local`；更高版本使用 `GOTOOLCHAIN=auto`，并同时解析 `go`、`toolchain` 指令。
- runtime/repository 模板配方分别升级到 `v4`/`v18`，保证不会命中旧错误模板缓存。
- 429 单独返回 `rate_limited`，等待 60 秒且不消耗仓库的三次普通错误重试；对应 Key 的有效并发会从 20 逐步降低，成功后恢复。
- 普通瞬时错误按 15/60/180 秒退避；`No space left on device` 单独记录为 `e2b_disk_exhausted`。
- 启动脚本使用幂等 marker 自动重入队今天受上述配方影响的失败仓库，同一修复版本不会重复重入队。

按修复完成时的最新 rejection 计算，下一次启动会补处理 234 个 Node 仓库和 31 个 Go 仓库，共 265 个。其中 4 个 Go 仓库已在 pending，脚本会新重入队其余 261 个。它们仍需重新通过构建、离线测试、benchmark 和包装，因此 265 不是最终新增 Task 数。

## 结论

有较大优化空间。修复前最值得优先处理的不是统一升级到 2 CPU / 4 GB，而是两处确定性的构建配方问题：

1. Node 项目无论使用 npm、pnpm 还是 Yarn，修复前都固定执行 `npm ci`。仅“缺少 `package-lock.json`”就造成 234 个仓库失败。
2. Go 把 `go.mod` 的 `go` 语言版本当成必须精确下载的工具链版本。32 个仓库因此产生 85 次 `infra_error`，且没有一个在重试后成功。

这两项合计影响 266 个仓库，但不能直接等同于 266 个新 Task；修复构建后，它们仍需通过离线测试、资源限制和 benchmark。

## 当前数据

| 指标 | 事件数 | 唯一仓库 | 占 2,430 个 E2B 入队仓库 |
| --- | ---: | ---: | ---: |
| 可交付 Task | - | 634 | 26.1% |
| `build_fail` | 902 | 897 | 36.9% |
| `e2b_resource_exhausted` | 405 | 346 | 14.2% |
| `infra_error` | 106 | 44 | 1.8% |

`build_fail` 按语言分布：Rust 277、TypeScript 216、Python 182、Go 135、JavaScript 87。

失败最多的构建步骤：

| 构建步骤 | 事件数 | 主要问题 |
| --- | ---: | --- |
| `npm ci` | 289 | 包管理器选错、缺少或不同步的 npm lockfile |
| `cargo build --tests` | 267 | 工具链/系统依赖、全 workspace 编译、下载或磁盘压力 |
| `pip install` | 162 | 原生 wheel、Python ABI、依赖体积和系统库 |
| `go build ./...` | 112 | 无差别构建所有包、CGO/系统库和平台专用代码 |
| Git checkout/submodule | 24 | SSH/private submodule 或不可访问依赖 |

另有 68 个 `build_fail` 明确包含 `No space left on device`，目前会被当作永久构建失败；增加内存不一定增加 E2B 构建盘，因此不能靠 2 CPU / 4 GB 自动解决。

## 根因

### 1. Node 配方没有识别包管理器

依赖哈希已经包含 `package-lock.json`、`pnpm-lock.yaml` 和 `yarn.lock`，但实际安装命令在 [recipes.py](../src/alvance_github_crawler/runtime/recipes.py) 中始终返回 `npm ci`。建议按以下顺序选择：

| 项目证据 | 安装命令 |
| --- | --- |
| `package-lock.json` / `npm-shrinkwrap.json` | `npm ci` |
| `pnpm-lock.yaml` 或 `packageManager=pnpm` | `corepack enable && pnpm install --frozen-lockfile` |
| `yarn.lock` 或 `packageManager=yarn` | 按 Yarn 版本使用 `--immutable` 或 `--frozen-lockfile` |
| 没有 lockfile | 标记为不可复现，或生成并持久化 lockfile；不要直接执行 `npm ci` |

这是当前最直接的通过率提升点，可覆盖 234 个确定的 missing-lock 失败。

### 2. Go 语言版本被误当成精确工具链

[profiles.py](../src/alvance_github_crawler/runtime/profiles.py) 会把 `go 1.18` 规范化为 `1.18.0`，再设置 `GOTOOLCHAIN=go1.18.0+auto`。但 `go` 指令表示最低语言版本，不等于仓库要求下载这个精确工具链。当前失败中，84/85 次工具链下载错误来自 Go 1.20 或更早版本。

建议分别解析 `go` 与 `toolchain` 指令：旧项目默认用受支持的本地 bootstrap Go 构建；只有显式 `toolchain goX.Y.Z` 时才精确选择工具链。修复后升级 runtime recipe 版本，避免复用已有的错误 `v3` alias，并重新入队这 32 个仓库。

### 3. 瞬时错误重试过快且分类不完整

44 个 `infra_error` 仓库产生了 106 次事件：27 个仓库重试 3 次、8 个重试 2 次，形成 62 次额外尝试。85 次其实是确定性的 Go runtime 错误；另有 14 次是 E2B 并发 429。当前队列会立即把错误项移到队尾，短队列时几乎等于立即重试，容易连续击中同一故障并停掉 key lane。

建议：

- 429、5xx、连接错误使用带抖动的退避，例如 15/60/180 秒；429 不计入仓库构建失败次数。
- 对每个 E2B Key 使用覆盖 build、offline sandbox、benchmark 和 wrapper smoke 的统一并发闸门。
- 发生 429 时临时从 20 降到 18-19，连续成功后再缓慢恢复到 20，而不是永久降低并发。
- 按错误指纹重试；同一个确定性错误只执行一次。
- 将 runtime 配方错误、仓库依赖错误、平台瞬时错误和磁盘/内存错误拆成独立 reason。

### 4. 构建目标过宽

Go 固定执行 `go build ./...`，Rust 固定执行 `cargo build --tests`。这会提前编译与任务方向无关的 workspace、示例、平台专用包和大体积依赖。可以利用已有 `direction_target_paths` 先定位 package/crate，只构建相关目标；最终离线测试仍需覆盖任务要求，不能为了通过率盲目缩小测试范围。

Python 还应综合 `requires-python`、tox/nox、CI matrix、本地 wheel ABI 和 lockfile 选择版本。当前已有 9 个明确的 Python wheel/ABI 不匹配，另有 59 个 Python 构建耗尽磁盘。

## 实施顺序

| 优先级 | 改动 | 预期收益 |
| --- | --- | --- |
| P0 | Node 包管理器与 lockfile 路由 | 直接处理 234 个 missing-lock 失败，提升潜在通过率 |
| P0 | 修复 Go `go`/`toolchain` 语义并升级 runtime recipe | 消除 85 次错误重试，重新验证 32 个仓库 |
| P0 | 瞬时错误退避、按 key 自适应并发、结构化错误码 | 减少 429 和 lane 停摆，节省 E2B 尝试 |
| P1 | `No space left` 独立分类与大依赖预判 | 避免 68 个确定性失败消耗完整构建时间 |
| P1 | Python ABI/CI 版本推断与常见系统依赖策略 | 改善 Python 原生依赖失败 |
| P1 | Go/Rust 按任务目标缩小 build 范围 | 降低编译时间、磁盘和内存长尾 |
| P2 | 记录 `failure_code`、命令、HTTP 状态、key slot、错误指纹 | 支持自动重试决策与监控统计 |

## 验收标准

- `infra_error` 唯一仓库占 E2B 入队比例从 1.8% 降到 0.5% 以下。
- 同一确定性错误指纹不再连续重试 2-3 次。
- Node missing-lock 不再以 `npm ci` 失败；改为正确包管理器或明确的不可复现拒绝。
- Go 1.20 及更早项目不再尝试下载不存在的 `goX.Y.0` 工具链。
- 429 项经过退避后可重新入队，不再因三次快速失败停掉整个 Key lane。
- 修复前后各连续运行至少两小时，对比 Task/h、E2B 注册率、每个 Task 消耗的 E2B 尝试数和 P90 验证耗时。

## 数据来源

- `outputs/github_production_500_unquota/rejections.jsonl`
- `outputs/github_production_500_unquota/pending.jsonl`
- `outputs/github_production_500_unquota/candidates.jsonl`
- `outputs/production-runs/*/logs/verify-*.log`
- `src/alvance_github_crawler/e2b/verification.py`
- `src/alvance_github_crawler/pending/verification.py`
- `src/alvance_github_crawler/runtime/profiles.py`
- `src/alvance_github_crawler/runtime/recipes.py`
