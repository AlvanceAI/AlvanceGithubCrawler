# wyy 与 XBY Harbor 样例生产整合计划

## 目标

把 wyy 与 XBY 两条开发线中对“生产 Harbor 样例”有实际收益的部分合并成一条可执行路线。整合后的目标不是只把代码拼在一起，而是形成三类可交付资产：

1. 可复现的 Harbor/Trace 三层产物：`catalog/`、`materials/`、`tasks/`，并保留 E2B 验证历史。
2. 面向生产筛选的质量信号：taskability、多样性、方向来源、潜在污染风险、反馈记录。
3. 面向 DeepSWE 任务制作的交接包：单仓库 handoff、repo summary、material/task 拷贝和可选源码 checkout。

## 已读代码与分支基线

共同祖先：

- `28469bd853f20add849b29b3b959ed93d931aca3`

分支状态：

- `main`：`2eca7a2fb2c70e5780d1359a270ef233a74724d4`，已包含 XBY 生产框架的大部分内容和 192 个可重建 package。
- `origin/XBY`：`6ccad51336e730bd33f0715aa22264f092d4645c`，在 `main` 之后继续加入三 Key 生产、GitHub token 池、原始 crawl 快照压缩归档和大量产物。
- `origin/wyy`：`82fab30526cb6534365f399656bf5daead8fad32`，主要新增 DeepSWE 交接、质量信号、反馈和导出工具。

重点阅读范围：

- wyy：`artifacts.py`、`deepswe_handoff.py`、`deepswe_feedback.py`、`diversity_report.py`、`material_export.py`、`production_events.py`、`repo_summary.py`、`taskability.py`，以及对 `cli.py`、`direction.py`、`harbor_task.py`、`trace_store.py`、`registry.py`、`candidate_registration.py` 的改动和对应测试。
- XBY：`crawl.py`、`pipeline.py`、`config.py`、`github.py`、`cli.py`、`pending/`、`e2b/`、`catalog/`、`runtime/python.py`、`run_report.py`、`monitor.py`、`scripts/run_continuous_production.sh`、`scripts/repair_rebuildable_tasks.py`，以及生产运行文档和 package repair 测试。

## 产物规模基线

| 来源 | package 数 | 语言分布 | 生产证据 | 结论 |
|---|---:|---|---|---|
| `main` | 192 | Go 92、JavaScript 16、Python 32、Rust 40、TypeScript 12 | 已有 rebuildable package repair 文档 | 是主线现状，但样例规模不足 |
| `origin/XBY` | 705 | Go 304、JavaScript 50、Python 94、Rust 182、TypeScript 75 | 2026-07-30 run 完整；2026-07-29 run 未完成但 pending 为 0 | 应作为 Harbor 样例产物主体 |
| `origin/wyy` | 9 | Go 2、Python 7 | 无大规模生产 run | 不作为产物主体，保留其质量和交接代码 |

交叉检查结果：

- `main` 的 192 个 package 全部包含在 `origin/XBY` 的 705 个 package 中。
- `origin/wyy` 的 9 个 package 也全部包含在 `origin/XBY` 中。
- 因此样例产物采用 XBY catalog 不会丢失 main 或 wyy 的 package。
- `origin/XBY` 的 705 个 package 中，599 个有 2026-07-30 完整 run 证据，87 个来自 2026-07-29 run，剩余约 19 个来自后续发布批次或补充提交，需要补充审计报告后再标记为完整闭环样例。

2026-07-30 XBY 完整 run 的关键数据：

- 原始 GitHub 样本：20,000。
- 初筛通过：9,989。
- E2B 队列：2,289。
- 可交付 Task：599。
- Pending：0。
- 资源分布：499 个 `1cpu-1024mb`，100 个 `2cpu-4096mb`。

## 总体取舍

核心判断：

- 以 XBY 作为结构和产物基座。原因是 XBY 已完成包结构重构、可恢复 crawl/produce/verify 分层、E2B 多 Key 消费、rebuildable Dockerfile 修复、监控和真实生产产物。
- 将 wyy 作为质量信号和 DeepSWE 交接层移植到 XBY 的新包结构中。原因是 wyy 解决的是“哪些样例更适合继续制作”和“如何交给下游生产”的问题，不应覆盖 XBY 已稳定运行的生产链路。
- 不采用 wyy 的旧扁平模块结构、Python 3.10 降级和小规模 package 产物。原因是当前主线已经改成 `catalog/`、`e2b/`、`pending/`、`runtime/`、`screening/` 子包，直接合并 wyy 会造成路径冲突和退化。

## 应采纳内容

### 来自 XBY 的内容

| 内容 | 决策 | 理由 |
|---|---|---|
| `catalog/`、`e2b/`、`pending/`、`runtime/`、`screening/` 子包重构 | 采纳为基座 | 模块边界清楚，当前 main 已采用该结构 |
| `crawl` 与 `produce` 分离 | 采纳 | 固定原始样本和 accepted JSONL，便于恢复和审计 |
| `PendingQueue` 与 `PendingVerificationRunner` | 采纳 | 允许 E2B 验证异步滚动消费，避免单仓库阻塞生产 |
| E2B 多 Key lane | 采纳并更新到 XBY 最新三 Key 版本 | 直接提升生产吞吐，且已有监控和测试 |
| GitHub 多 token 池与 `_GitHubTokenClient` | 采纳 | 释放旧版全局 HTTP 锁，支持并发预筛 |
| `run_continuous_production.sh` 和 `monitor.py` | 采纳 | 已覆盖启动、恢复、发布、报告和终端监控 |
| `package_repair.py` | 采纳 | 使旧 E2B fingerprint 包升级为可重建 Dockerfile，是 Harbor 长期可用的关键 |
| `run_report.py` 和生产 Markdown | 采纳 | 为样例集提供可审计的漏斗、耗时和性能证据 |
| 705 个 XBY package 产物 | 采纳为完整资产池 | 覆盖五种语言，且包含 main 和 wyy 的 package |
| 原始 crawl JSONL gzip 归档 | 采纳 | 保留恢复能力，同时避免提交大体积原始 API payload |

### 来自 wyy 的内容

| 内容 | 决策 | 理由 |
|---|---|---|
| `taskability.evaluate_taskability` | 采纳，作为选择信号 | 能过滤文档/示例类低价值方向，适合 Harbor 样例精选 |
| `contamination` 元数据 | 采纳但改弱约束 | public issue 只能说明方向来源公开，不能直接证明污染；应作为审计字段和人工复核提示 |
| `deepswe_handoff.py` | 采纳并适配当前 catalog schema | 下游需要单候选 handoff JSON，不应让 DeepSWE 生产直接读整条 candidate/catalog |
| `repo_summary.py` | 采纳 | 为低 token repo-card 或人工筛查提供紧凑输入 |
| `material_export.py` | 采纳并扩展 | 可把 candidate、handoff、summary、materials、tasks 组织为交接目录 |
| `diversity_report.py` | 采纳 | 用于检查语言、owner、路径类别和质量分布，避免样例集偏斜 |
| `deepswe_feedback.py` | 采纳 | 让下游制作结果回写，形成候选质量闭环 |
| `production_events.py` | 采纳 | 给 registry 注册和拒绝事件补充机器可读事件流 |
| Responses API 到 Chat Completions 回退 | 采纳 | OpenAI 兼容网关可能不支持 Responses API，回退能降低 Stage 3 中断率 |
| SOCKS proxy doctor 检测和 `PySocks` | 采纳为运行环境增强 | 生产网络环境可能需要 SOCKS 代理，doctor 应在消耗额度前提示 |
| Harbor instruction scaffold 标注 | 采纳 | 明确当前 Task 是方向 scaffold，不是最终 DeepSWE task spec |
| `dirhash` 缺失 fallback | 可采纳 | `dirhash` 已是依赖，但 fallback 能提升脚本在裁剪环境中的可恢复性 |

## 不采纳或暂缓内容

| 内容 | 处理 | 原因 |
|---|---|---|
| wyy 的旧扁平路径导入，例如 `candidate_registration.py`、`harbor_task.py`、`trace_store.py` | 不直接合并 | 当前已迁移到 `pending/registration.py` 和 `catalog/*` |
| wyy 的 Python 3.10 降级 | 不采纳 | 当前 XBY 代码使用 `tomllib` 并以 Python 3.11 为目标；降级会扩大测试和兼容成本 |
| wyy 的简易 TOML parser | 暂缓 | Python 3.11 有标准 `tomllib`，无需引入不完整解析器 |
| wyy 的小规模 package 产物 | 不作为生产主体 | 9 个 package 已被 XBY 705 包含，无需重复维护 |
| wyy 把 issue 来源一律标记为 `contamination.risk=medium` | 调整 | 这个信号过粗，应用于人工提示，不应用于自动剔除 |
| 直接把 wyy CLI flag 全部塞进当前顶层 parser | 不建议 | 当前 CLI 已较拥挤，建议做成清晰子命令，并保留旧 flag 兼容 |
| XBY 的 2026-07-31 发布批次直接标记为完整闭环 | 暂缓 | 分支中没有对应 run metrics 文档，需补审计报告 |
| 继续提交未压缩 `raw_repositories.jsonl` | 不采纳 | 体积大且包含原始 API payload，保留 gzip 和本地恢复即可 |

## 路径映射

wyy 到当前主线的移植映射：

| wyy 路径 | 当前目标路径 | 说明 |
|---|---|---|
| `src/alvance_github_crawler/candidate_registration.py` | `src/alvance_github_crawler/pending/registration.py` | 增加 taskability 和 contamination 字段 |
| `src/alvance_github_crawler/direction.py` | `src/alvance_github_crawler/screening/direction.py` | 在 XBY 重试逻辑上增加 Chat Completions fallback |
| `src/alvance_github_crawler/harbor_task.py` | `src/alvance_github_crawler/catalog/harbor_task.py` | 增加 scaffold 说明、solve placeholder、hash fallback |
| `src/alvance_github_crawler/trace_store.py` | `src/alvance_github_crawler/catalog/trace_store.py` | solve placeholder 和 hash fallback |
| `src/alvance_github_crawler/trace_materials.py` | `src/alvance_github_crawler/catalog/trace_materials.py` | 当前 main 已使用 Python 3.11 的 `UTC`，不需要 timezone 替换 |
| `src/alvance_github_crawler/python_install.py`、`python_workspace.py` | `src/alvance_github_crawler/runtime/python.py` | 只评估具体安装逻辑，不移植 Python 3.10 parser |
| `src/alvance_github_crawler/material_export.py` | 保持顶层或新建 `handoff/material_export.py` | 需要适配 XBY catalog schema 和 production dir |
| `deepswe_*`、`repo_summary.py`、`diversity_report.py`、`taskability.py` | 可保持顶层，也可放入 `handoff/` 子包 | 若新增子包，CLI 和测试一起更新 |
| `production_events.py` | 顶层共享模块 | `registry.py`、CLI 和 run report 都可复用 |

## 目标数据流

整合后数据流如下：

```text
GitHub crawl
  -> accepted_repositories.jsonl
  -> produce/prescreen
  -> pending.jsonl
  -> E2B offline + benchmark
  -> CandidateRegistrar
  -> candidates.jsonl with quality signals
  -> HarborPackager
  -> catalog/materials/tasks
  -> run_report + diversity_report
  -> DeepSWE handoff/material export
  -> downstream feedback.jsonl
```

关键原则：

- `candidates.jsonl` 保存生产决策和质量信号。
- `catalog/e2b-packages.jsonl` 保存 Harbor 可复现和验证历史，不承担全部人工筛选字段。
- `tasks/*` 与 `materials/*` 保存可重建 Dockerfile、测试入口和最小 Trace 封装，不保存源码 checkout。
- DeepSWE handoff/export 是派生产物，可以放在 `outputs/deepswe-handoff/<run_id>/`，默认不提交源码。

## 分阶段实施计划

### Phase 0，建立整合分支和保护基线

1. 从 `main` 创建整合分支，例如 `integration/wyy-xby-harbor-samples`。
2. 记录当前三条引用：`main`、`origin/XBY`、`origin/wyy`。
3. 确认工作区干净，避免覆盖未提交的人工改动。
4. 先跑轻量检查：`uv run pytest tests/test_package_repair.py tests/test_harbor_packaging.py tests/test_config.py`。

验收：

- 当前 main 测试基线明确。
- 没有未解释的工作区改动。

### Phase 1，前移 XBY 生产基座

1. 将 `origin/XBY` 合入整合分支。由于 `origin/XBY` 是当前 `main` 的后继，优先用 fast-forward 或普通 merge 保留历史。
2. 确认以下 XBY 后续改动存在：
   - `PipelineConfig.github_tokens` 和编号 `GITHUB_TOKEN<n>` 解析。
   - 编号 `E2B_API_KEY<n>` 动态解析，至少支持 `E2B_API_KEY1/2/3`。
   - `GitHubClient` round-robin token lane 和线程本地 session。
   - `doctor` 输出 `github_token_count`。
   - `scripts/run_continuous_production.sh` 需要 `gzip`，发布前压缩 `raw_repositories.jsonl`。
   - `monitor.py` 显示 GitHub token 数和持续生产状态。
3. 保留 XBY 的 705 个 package、对应 `materials/`、`tasks/`、`catalog/`。
4. 对 2026-07-29、2026-07-30 run 文档和 outputs 做审计标注：
   - 2026-07-30：完整 run，可作为主要证据。
   - 2026-07-29：crawl 状态 incomplete，但 pending 为 0，产出的 87 个任务可作为已验证补充。
   - 后续无 metrics 的批次：先进入候选资产池，补报告前不作为闭环样例宣传。

验收：

- `git show HEAD:catalog/e2b-packages.jsonl | wc -l` 为 705。
- `uv run python scripts/repair_rebuildable_tasks.py --root . --check --workers 8` 通过。
- `uv run pytest tests/test_config.py tests/test_github.py tests/test_monitor.py tests/test_package_repair.py` 通过。

### Phase 2，移植 wyy 质量信号

1. 新增或移植 `taskability.py`，但把它作为 selection signal，不作为硬拒绝条件。
2. 修改 `pending/registration.py`：
   - 在注册最终 candidate 时写入 `taskability`。
   - 写入 `contamination`，字段建议包含：
     - `direction_source`
     - `keywords`
     - `h6_sources`
     - `public_issue_inspiration`
     - `risk`
     - `notes`
   - 对 `risk` 使用保守默认 `unknown`，只有明确命中高风险规则时再提升。
3. 修改 `catalog/package_models.py`：
   - 对新生成 package 记录保留可选 `quality` 字段，包含 taskability、contamination 和 direction metadata。
   - 不要求历史 705 个 package 立即回填该字段，避免无谓 churn。
4. 修改 `pipeline.py` 和 `pending/verification.py`：
   - `JsonlRegistry` 接收可选 `events_path=config.output_dir / "events.jsonl"`。
   - 注册、拒绝、反馈、导出都写 machine-readable events。
5. 修改 `registry.py`：
   - 保留当前 `append_text_locked` 和 `_write_lock`。
   - 加入 wyy 的 `ProductionEventWriter`，但事件写入失败不应中断主流程。
6. 添加测试：
   - `test_candidate_registration_persists_taskability_and_contamination`
   - `test_production_events_can_be_read_after_registry_actions`
   - 回归 `test_pending_verification.py`，确认事件 hook 不破坏多 Key verifier。

验收：

- 新 candidate 记录包含 `taskability` 和 `contamination`。
- registry 事件流能重放注册和拒绝。
- 旧 catalog package 没有新增字段时仍能被 `package_repair --check` 接受。

### Phase 3，移植 DeepSWE handoff 与导出工具

1. 移植 `artifacts.py`、`deepswe_handoff.py`、`repo_summary.py`、`deepswe_feedback.py`、`diversity_report.py`。
2. 重写 `material_export.py` 的 record loader，使其支持当前 XBY 布局：
   - `--production-dir`，默认 `config.output_dir`，读取 `candidates.jsonl`。
   - `--catalog-dir`，默认 `config.catalog_dir`，读取 `e2b-packages.jsonl`。
   - `--crawler-root`，默认仓库根目录，用于复制 `materials/` 和 `tasks/`。
3. 适配当前 package schema：
   - Harbor template alias/id 从 `e2b_history.harbor_template` 读取。
   - source template 从 `e2b_history.source_template` 读取。
   - launch command 从 `harbor.launch_command` 读取。
   - `material_path`、`task_path` 使用 package 顶层字段。
4. 输出目录建议：

```text
outputs/deepswe-handoff/<run_id>/
├── index.json
├── selected-candidates.jsonl
├── handoff/
├── repo-summary/
├── materials/
├── crawler-tasks/
└── repos/                  # 仅用户显式 --clone-repos 时生成
```

5. CLI 建议增加子命令，同时兼容 wyy 旧 flag 一段时间：
   - `alvance-github-crawler export-handoff --repo owner/name --out ...`
   - `alvance-github-crawler export-repo-summary --repo owner/name --out ...`
   - `alvance-github-crawler export-materials --repo-count 100 --out outputs/deepswe-handoff/...`
   - `alvance-github-crawler diversity-report --out ...`
   - `alvance-github-crawler feedback --repo ... --base-commit ... --outcome ... --reason ...`
   - `alvance-github-crawler events --tail 100`

验收：

- wyy 的 `test_deepswe_handoff.py`、`test_repo_summary.py`、`test_material_export.py`、`test_diversity_report.py`、`test_deepswe_feedback.py` 在新路径下通过。
- 从 XBY 705 catalog 中选择 5 个仓库，可以导出 handoff、summary、material/task copy。
- 默认不 clone 源码，网络隔离环境也能产出交接包。

### Phase 4，合并方向判定兼容性

1. 在 `screening/direction.py` 中保留 XBY 的共享限速和 retry：
   - `MAX_ATTEMPTS`
   - `_wait_for_request_window`
   - `_defer_requests`
   - `_is_retryable_openai_error`
   - `_openai_retry_delay`
2. 加入 wyy 的 Responses API 不可用 fallback：
   - 如果 `responses.parse` 返回 404 或明确的 page-not-found，切换到 Chat Completions。
   - 如果 `response_format={"type": "json_object"}` 不被支持，再退到普通文本并抽取 JSON object。
   - fallback 输出必须经过 `DirectionVerdict.model_validate`。
3. 对 fallback 也套用同一套 retry 和节流，避免模型网关故障时放大请求。
4. 增加测试：
   - Responses 404 时调用 Chat Completions。
   - Chat JSON mode 不支持时仍能从文本提取 JSON。
   - 429/502 仍按 XBY 重试逻辑退避。

验收：

- 现有 `tests/test_direction.py` 全部通过。
- 新增 wyy fallback 测试通过。
- 不降低 H6 失败关闭语义，搜索异常仍然不当作零结果放行。

### Phase 5，强化 Harbor task 语义

1. 修改 `catalog/harbor_task.py`：
   - `render_instruction` 开头标明这是 Crawler-produced direction scaffold。
   - 保留 `task.toml` 中 `metadata.status = "direction"`。
   - `render_test_script` 不变，保持 Harbor verifier 可执行。
2. 修改 `catalog/trace_store.py`：
   - `solution/solve.sh` 写入 placeholder 注释，避免误认为是 reference solution。
3. `dirhash` fallback：
   - 可在 `harbor_template_alias` 和 `TracePackageStore.prepare` 中加入纯标准库 hash。
   - `package_repair.py` 仍可继续依赖 `dirhash`，因为它是项目依赖且用于审计。

验收：

- `tests/test_harbor_task_direction_scaffold.py` 通过。
- 已有 `tests/test_harbor_packaging.py`、`tests/test_package_repair.py` 通过。
- 对新生成 task，`instruction.md` 不再让下游误读为最终 DeepSWE 题面。

### Phase 6，配置与运行环境整合

1. 保留 `requires-python = ">=3.11"`。
2. 保留 XBY 的 `rich` 依赖，用于 `monitor.py`。
3. 加入 `PySocks>=1.7,<2`，或作为可选 extra `proxy`。如果生产环境常用 SOCKS，建议直接放入基础依赖。
4. `doctor` 增加：
   - `github_token_count`
   - `socks_proxy_configured`
   - `socks_support`
5. `.env.example` 保留 XBY 的编号 token/key 格式：
   - `GITHUB_TOKEN1`、`GITHUB_TOKEN2`
   - `E2B_API_KEY1`、`E2B_API_KEY2`、`E2B_API_KEY3`
   - 单 Key fallback 仍保留。

验收：

- `uv run alvance-github-crawler --doctor` 不泄露任何 key。
- 设置 SOCKS 代理但缺少 `PySocks` 时，doctor 能明确提示。
- `tests/test_config.py` 覆盖 GitHub token 数字排序和 E2B 三 Key。

### Phase 7，构建 Harbor 样例分层

不建议把 705 个 package 都作为“人工制作优先样例”。应分三层：

| 层级 | 数量建议 | 选择规则 | 用途 |
|---|---:|---|---|
| Full asset pool | 705 | XBY catalog 全量，通过 package repair audit | 可复现 Harbor 资产池 |
| Production sample pool | 200 左右 | 五语言均衡、owner 去重、`ready_for_phase1` 优先、taskability 高、无高风险 contamination、性能在预算内 | 给 DeepSWE 生产队列 |
| Smoke/demo set | 25 左右 | 每语言 5 个，优先 1 CPU/1024 MB、stable、测试低于 60 秒 | 快速验收和演示 |

推荐选择分数：

```text
sample_score =
  adjusted_score
  + taskability.score
  + 3 if benchmark.offline_ok
  + 2 if benchmark.stable
  + 1 if test_duration_median_s <= 30
  - contamination_risk_penalty
  - owner_dup_penalty
  - resource_cost_penalty
```

选择约束：

- 每种语言至少占 15%，最多占 30%，Smoke set 固定每语言 5 个。
- 单 owner 在 Production sample pool 中默认最多 3 个。
- `status=ready_for_phase1` 优先；`ready_for_phase1_flaky_test_suite` 只进入备选。
- `2cpu-4096mb` 保留一小部分用于覆盖重资源样例，但不进入 Smoke set。
- `direction_target_paths` 全在 `docs/`、`examples/`、`website/` 时降权。

验收：

- `diversity-report.md` 中没有语言超过 40%。
- Smoke set 可在有限时间内运行 `harbor run --no-force-build` 抽查。
- 每个入选项都有 handoff、summary、catalog record、task path 和 material path。

## 具体冲突与解决方案

### CLI 冲突

当前 XBY CLI 已有 positional command：`crawl`、`produce`，同时保留 `--verify-pending`、`--package-existing`、`--requeue-failures` 等顶层模式。wyy 增加多个顶层 flag 会继续扩大互斥复杂度。

解决：

- 短期：保留 wyy flag 作为兼容入口，降低迁移成本。
- 中期：新增显式子命令，例如 `export-handoff`、`export-materials`、`feedback`、`events`。
- 测试覆盖旧 flag 和新子命令，文档只推荐新子命令。

### Catalog schema 冲突

wyy 的 `material_export.py` 从 `harbor.template_alias`、`harbor.template_id` 读取模板信息；XBY 的 rebuildable schema 把 operational template 信息放入 `e2b_history.harbor_template`，`harbor` 下只保留 launch/smoke/build_source。

解决：

- `e2b_metadata()` 优先读取 `e2b_history.harbor_template`。
- fallback 支持旧 schema，便于读取历史 candidates。
- 导出 handoff 时明确 `operational_dependency=false`，避免下游误以为 alias 是唯一运行依据。

### Registry 写入冲突

XBY registry 使用锁和 `append_text_locked`，wyy 版本没有锁但有事件。生产并发下必须保留 XBY 写入方式。

解决：

- 在 XBY `JsonlRegistry` 中新增可选 `events_path`。
- register/reject 成功写主 JSONL 后再 emit event。
- event 写失败只记录 warning，不影响候选注册。

### 方向模型冲突

XBY 提供 retry 和共享退避，wyy 提供 API fallback。两者都需要。

解决：

- 把 wyy fallback 包进 XBY retry loop。
- 只对 Responses API 不支持做永久 fallback；对 429、502、timeout 仍按 retry 处理。
- fallback JSON 必须 schema validate。

### Python 版本冲突

wyy 为兼容 Python 3.10 加了简易 TOML parser；XBY 保持 Python 3.11。

解决：

- 不降级 Python 要求。
- 不引入简易 TOML parser。
- 若将来必须支持 Python 3.10，应使用 `tomli`，不要维护半解析器。

## 最终验收清单

代码验收：

- `uv run pytest`
- `uv run ruff check .`
- `bash -n scripts/run_continuous_production.sh`
- `bash -n run.sh`
- `git diff --check`

产物验收：

- `uv run python scripts/repair_rebuildable_tasks.py --root . --check --workers 8`
- `catalog/e2b-packages.jsonl` 为有效 JSONL，且 package_id 无重复。
- `catalog/repo-materials.toml` 与 JSONL 数量一致。
- `tasks/*/environment/Dockerfile` 与 `materials/*/environment/Dockerfile` 一致。
- 每个 package 的 Dockerfile 包含 `base_commit`、`source_tree` 和依赖安装命令。
- `harbor.template_id`、`harbor.template_alias` 不再作为 operational metadata 留在 `harbor` 顶层。

DeepSWE 交接验收：

- 对至少 5 个不同语言样例执行 handoff 导出。
- 每个 handoff 包含 `repo`、`repository_url`、`base_commit`、`source_tree`、`language`、`direction`、`test_cmd`、`material_path`、`task_path`、`taskability`、`contamination`。
- `repo-summary` 能在不读取源码的情况下给出紧凑 metadata。
- `diversity-report.md` 能统计语言、owner、taskability、contamination 和路径类别。
- `feedback.jsonl` 可追加并按 `(repo, base_commit)` 读取最新结果。

生产验收：

- `uv run alvance-github-crawler --doctor` 显示 GitHub token 数、E2B key 数、总并发、SDK 状态和 SOCKS 状态。
- `monitor.py` 能启动 driver，并在日志中记录 run id、batch、prescreen concurrency 和 E2B concurrency。
- `run_continuous_production.sh` 发布报告时压缩 raw crawl snapshot，并能从 `.gz` 恢复本地 checkpoint。
- 抽样执行 `harbor run --path tasks/<task> --env e2b --no-force-build --agent nop --disable-verification`，确认 wrapper alias 或 rebuildable Dockerfile 路径可用。

## 推荐落地顺序

1. 先合 XBY 最新生产基座和 705 package，建立完整 Harbor 资产池。
2. 再移植 wyy 的质量信号到 candidate 注册路径，不立即回填所有历史 package。
3. 移植 handoff、repo summary、diversity、feedback 和 event 工具。
4. 合并方向模型 fallback 与 SOCKS doctor，降低生产中断。
5. 用导出工具生成 Production sample pool 和 Smoke/demo set。
6. 补一份样例集审计报告，说明选择规则、数量、语言分布、资源分布、已知风险和复测命令。

## 需要补充的文档

建议新增或更新：

- `docs/harbor-sample-set-selection.md`：记录 705 全量池、200 生产池、25 smoke set 的选择规则和最终列表。
- `docs/deepswe-handoff-runbook.md`：说明如何从 catalog/candidates 导出 handoff、summary 和 material bundle。
- `docs/continuous-production-github-mass-production-XBY-20260731.md`：若保留 20260731 批次，需要补齐 metrics 和统计文档。
- `README.md`：增加 DeepSWE handoff 子命令和 sample set 快速验收命令。

## 风险

- GitHub 多 token 若属于同一账号，GitHub 可能仍共享账号级额度；doctor 只能证明 token 存在，不能保证额度独立。
- Chat Completions fallback 可能输出非严格 JSON；必须 schema validate，失败时保持当前 fail-closed 行为。
- `taskability` 是启发式信号，不能直接替代人工判断；短期只用于排序和 report。
- `contamination` 字段的命名容易被误解；文档要说明它是公开来源和复核提示，不是最终污染判定。
- 705 个 package 语言分布偏向 Go 和 Rust；对外展示或人工生产队列必须用多样性选择层再筛一次。
- E2B historical alias 可能过期；rebuildable Dockerfile 是长期保障，抽查必须覆盖 alias miss 后重建路径。

## 结论

最优合并路线是“XBY 负责生产骨架和产物池，wyy 负责质量信号和 DeepSWE 交接”。直接把 wyy 分支整体 merge 到当前主线会回退包结构并引入冲突；直接只用 XBY 又缺少人工生产所需的筛选、反馈和 handoff 工具。按上述阶段合并后，仓库会同时具备大规模 Harbor 可复现样例、可解释的候选质量信号，以及能交给 DeepSWE 生产流程的稳定导出格式。
