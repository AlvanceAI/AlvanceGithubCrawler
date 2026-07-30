# E2B 模板失效修复报告

日期：2026-07-30

## 结论

已修复现有 192 个可交付 Task 及其 192 个 material。Task 不再把 E2B alias/template ID 当作运行前提；Harbor 找不到旧 alias 时，会从仓库内的真实 `environment/Dockerfile` 重建。

## 修复前

- 192 个 Dockerfile 都是 `FROM e2bdev/base` 的不可构建指纹文件。
- Task 和 material 标记为 `e2b-only`，catalog 标记为 `remote_e2b_only=true`。
- 运行记录中的 E2B alias/template ID 是唯一可用环境来源，过期后无法重建。
- Python 的安装命令没有持久化，无法可靠恢复每个项目的测试依赖。

## 修复后

- 192/192 个 Task 和 material 都有相同的真实 Dockerfile。
- Dockerfile 包含版本化语言运行时、系统包、GitHub 精确 commit 和 tree 校验、递归 submodule 初始化，以及与 E2B 完全相同的依赖/构建命令。
- 192 条 catalog 记录全部写入 `dependency_commands`，其中 32 个 Python 项目从精确 commit 重新解析，Go 92、Rust 40、JavaScript 16、TypeScript 12 使用确定性配方。
- Task metadata 改为 `storage_mode="dockerfile-rebuildable"`，并显式记录 `dockerfile_rebuildable=true`、`rebuild_network_required=true`。
- catalog 的 `remote_e2b_only` 已全部改为 `false`。
- 旧 E2B ID 仍保存在 `e2b_history` 和 `receipts/e2b.json` 中，仅作验证历史/缓存提示，不参与启动决策。
- Task ID 保持原样，避免下游引用失效。

## 实际修复样例

样例来自本次真实产出的 Python Task：

- 仓库：`mirumee/ariadne-codegen`
- Task：`tasks/alv-ariadne-codegen-11c5b0-083d1802-v2`
- 精确 commit：`083d18025137bc3e6359cad61bafb9929563ab75`
- 精确 source tree：`600bfff9cb7b82171573d7492ed5fc2f3524cb23`
- 历史 E2B alias：`alv-ariadne-codegen-11c5b0-083d1802-v2-env-b8df7bdc`
- 历史 E2B template ID：`fu3j9961jsbn0zjpz9x4`

修复前的 Dockerfile 只有环境指纹：

```dockerfile
# Harbor envelope v2
# Source E2B template: t5cea841kz35bqc1vpba
# This file is an immutable Harbor fingerprint; do not force-build it.
FROM e2bdev/base
USER root
WORKDIR /app
```

这份文件没有源码地址、commit 或依赖安装命令。历史 alias/template ID 一旦失效，Harbor 即使读到 Dockerfile 也无法恢复原环境。

修复后的真实文件位于 `tasks/alv-ariadne-codegen-11c5b0-083d1802-v2/environment/Dockerfile`，关键内容如下：

```dockerfile
FROM docker.io/library/python:3.11
USER root
ENV HOME="/home/user"

RUN apt-get update && apt-get install -y --no-install-recommends \
    time git ca-certificates build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN rm -rf /app && mkdir -p /app && git init /app && cd /app \
    && git remote add origin https://github.com/mirumee/ariadne-codegen.git \
    && git fetch --depth=1 origin 083d18025137bc3e6359cad61bafb9929563ab75 \
    && git checkout --detach FETCH_HEAD \
    && git submodule update --init --recursive \
    && test "$(git rev-parse HEAD)" = 083d18025137bc3e6359cad61bafb9929563ab75 \
    && test "$(git rev-parse HEAD^{tree})" = 600bfff9cb7b82171573d7492ed5fc2f3524cb23

WORKDIR /app
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir -e '.[test,dev]'
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
```

对应 metadata 的实际变化：

| 字段 | 修复前 | 修复后 |
| --- | --- | --- |
| `storage_mode` | `e2b-only` | `dockerfile-rebuildable` |
| `remote_e2b_only` | `true` | `false` |
| `dependency_commands` | 未保存 | 保存上述两条 `pip` 命令 |
| 当前环境 SHA-256 | `b8df7bdc...` | `6bfae594...` |
| E2B alias/ID | 运行依赖 | 仅存于 `e2b_history` 和 receipt |

当历史 alias 被删除或过期后，执行现有 launch command 时，Harbor 会发现当前环境 alias 不存在，随后从上述 Dockerfile 创建模板：拉取精确 commit、核对 tree、安装已经持久化的依赖，再进入 `/app`。因此历史 E2B template 不再决定这个 Task 是否可运行。

## 代码改动

- `runtime/recipes.py`：E2B 模板和 Dockerfile 共用运行时、checkout、依赖安装和收尾配方。
- `catalog/harbor_task.py`：生成可重建 Dockerfile 和新 metadata。
- `catalog/package_repair.py`、`scripts/repair_rebuildable_tasks.py`：幂等回填和审计脚本。
- `scripts/run_continuous_production.sh`：每次量产启动前自动执行回填/审计，避免旧格式再次进入生产。

## 验证

- 回填：`checked=192 changed=192`。
- 第二次审计：`checked=192 changed=0 unchanged=192`。
- Task/material Dockerfile 不一致数：0。
- `FROM e2bdev/base` 数量：0。
- `storage_mode="e2b-only"` 数量：0。
- `mode="e2b-only"` 数量：0。
- `remote_e2b_only=true` 数量：0。
- `uv run pytest -q`：全部通过。
- `uv run ruff check .`、`bash -n scripts/run_continuous_production.sh`、`git diff --check`：通过。
- 本机 Docker daemon 权限不足（`/var/run/docker.sock` denied），因此未能执行真实镜像构建；Dockerfile 内容审计和跨文件哈希审计已完成。

重建仍需要访问 GitHub 精确 commit 和语言包注册表，这是预期的外部依赖；E2B alias/template 过期不再是阻断条件。

## 手动启动完整管线

项目目前保持暂停。确认 `.env` 中的 GitHub/OpenAI/E2B 凭据后，一条命令启动搜索、筛选、双 Key E2B 并发验证、Task 生成和 XBY 发布：

```bash
cd /home/xubingyu/AlvanceGithubCrawler
uv run python monitor.py
```

启动脚本会先审计/修复历史包，然后按现有配置使用每个 E2B key 最多 20 并发；三把 Key 时总并发为 60；不会在本次修复过程中自动启动生产。
