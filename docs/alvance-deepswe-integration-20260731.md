# AlvanceDeepSWE 联调说明（2026-07-31）

## 联调基准

- 下游仓库：`AlvanceAI/AlvanceDeepSWE`
- 固定分支：`feature/three-roll-stable`
- 当前提交：`e6db6f14ed04b1991b0e9dbde085c5564d84c907`
- 上游仓库：`AlvanceGithubCrawler`，兼容修改优先在本仓库完成。

DeepSWE 从 Crawler 的 `tasks/<task-id>`、`materials/<material-id>` 和 candidate
JSONL 发现并导入合格任务。candidate 优先读取本地 `.crawler-state/candidates.jsonl`，
同时兼容已发布的 `outputs/*/candidates.jsonl`。E2B 历史模板只作为验证记录，实际运行
环境必须能从 `environment/Dockerfile` 重建。

## 接口契约

Crawler 交付项必须同时满足：

1. candidate 状态为 `ready_for_phase1` 或 `qualified`，且 direction 非空；
2. material 声明 `mode = "dockerfile-rebuildable"`、规范 Dockerfile 路径和完整环境哈希；
3. task 与 material 的 Dockerfile 内容及 `dirhash` 完全一致；
4. source 包含完整 base commit 和 source tree；
5. material 包含 baseline 与 `scripts/export-patch.sh`，供 DeepSWE 安装 `pre_artifacts.sh`；
6. Dockerfile 可被 Docker、Harbor 和 E2B SDK 的 `from_dockerfile()` 一致解析。

## Dockerfile 兼容修复结果

问题位于 Crawler 与 DeepSWE/E2B 的解析边界：Docker 接受顶层 `#` 注释，但当前 E2B
SDK 的 `from_dockerfile()` 会将其识别为 `COMMENT` 指令；严格解析时该指令不受支持，
导致 DeepSWE 无法从交付的 Dockerfile 重建模板。

修复前：

```dockerfile
# Harbor rebuildable envelope v2
# Dockerfile recipe v3
# E2B aliases are optional caches; this file is the durable build source.
FROM python:3.12
USER root
WORKDIR /app
```

修复后：

```dockerfile
FROM python:3.12
USER root
WORKDIR /app
```

Crawler 生成器现已移除顶层注释，并在生成时使用 E2B 指令白名单拒绝 `COMMENT` 等
不兼容指令。`2026-07-31` 批量修复已同步更新 705 个 task、705 个 material、环境哈希、
TOML 和 catalog；修复后当前 E2B SDK `from_dockerfile()` 实际解析结果为 705/705 通过。

## 当前风险

- COMMENT 兼容问题已在当前工作树完成迁移。发布时必须同时提交 task、material 和 catalog，
  不能只提交 Dockerfile，否则下游会看到环境哈希不一致。
- 批量修复逐文件更新 task、material 和 manifest；本次迁移期间已暂停生产和下游扫描。
  后续大规模迁移仍应从完成并提交的稳定快照交付。
- DeepSWE 原先声明 Python `>=3.11`，但其 Harbor 依赖要求 `>=3.12`，会令干净环境的
  `uv sync` 解算失败；联调分支已将下限校正为 `>=3.12`。
- PyPI Harbor `0.1.42` 至 `0.1.45` 会解析但忽略 delivery 使用的 `artifacts`、
  `verifier.separate` 和 `environment_mode` 扩展字段。本地 Roll 管线没有启用 verifier，
  但最终 separate-verifier 归档仍须在目标评测环境做一次真实回放，不能仅以本地
  `TaskConfig` 解析成功作为兼容证明。
- 联调还需覆盖发现、导入、Dockerfile 哈希校验、提交脚本复制和一次真实模板重建；仅跑
  Crawler 单元测试不能证明下游可用。

## 完成标准

- Crawler 新生成的 durable Dockerfile 不含 COMMENT 节点；
- 两仓测试覆盖同一份合成任务的“生成 -> 发现 -> 导入”流程；
- DeepSWE 能发现任务并保持 Dockerfile、environment hash、base commit 和提交脚本一致；
- Crawler 全量测试与 DeepSWE 相关测试通过；真实 E2B 未执行时必须单独记录限制。
