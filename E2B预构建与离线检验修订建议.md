# E2B 预构建与离线检验修订建议

## 文档状态

- 状态：提案，尚未合并进《仓库收集与检验管线 — 最终方案》
- 影响范围：Stage 4、Stage 5，以及二者之前的执行环境准备
- 不影响：Stage 0–3 的候选抓取、硬过滤、软评分和方向核查
- 已确认决策：E2B Repository Template 首次构建不设置淘汰超时，仅记录耗时；600 秒只用于断网测试。

## 背景与问题

当前 Stage 4 把以下开销全部放进单个 `docker build timeout=600`：

- 拉取基础镜像；
- 安装 `apt` 系统包；
- 下载语言运行时或编译器工具链；
- 下载仓库依赖；
- 编译仓库；
- 准备离线测试环境。

这会把基础设施网络速度误判成仓库不可用。例如仓库本身能够编译，但首次拉取 Go/Python/Node/Rust 镜像或工具链超过 10 分钟，最终被标记为 `build_timeout`。这类结果属于基础设施假阴性，不应进入仓库质量判定。

E2B SDK 已支持：

- `Template.from_dockerfile(...)`：从 Dockerfile 预构建模板；
- `Template.from_image(...)`：从远端镜像仓库导入镜像；
- `Template.from_template(...)`：从基础模板继续构建仓库模板；
- `Template.build(..., alias=..., skip_cache=False)`：持久化并复用构建缓存；
- `Sandbox.create(template=..., allow_internet_access=False)`：从模板启动断网 Sandbox。

因此建议把工具链和依赖准备从 H5 判定中拆出，使用 E2B Template 作为持久执行环境。

## 分层定位

建议新增一个位于 Stage 3 与 Stage 4 之间的基础设施层：

```text
Stage 3    方向可行性核查
    ↓
Stage 3.5  E2B 执行环境预构建（基础设施层，不参与仓库判定）
    ↓
Stage 4    Repository Template 断网测试（H5）
    ↓
Stage 5    复用同一 Template 做执行开销基准
```

Stage 3.5 不计入软评分、H5 的 10 分钟阈值或 Stage 5 冷启动时间。

## 两级 Template 设计

### Runtime Template

按以下键复用：

```text
(language, runtime_version, architecture, runtime_recipe_version)
```

示例 alias：

```text
alvance-go-1-26-5-amd64-v1
alvance-python-3-12-amd64-v1
alvance-node-22-amd64-v1
alvance-rust-1-88-amd64-v1
```

Runtime Template 负责预装：

- 正确版本的语言运行时和编译器；
- `/usr/bin/time`；
- 常见系统构建工具；
- 可达的软件包代理；
- 与具体仓库无关的公共环境配置。

运行时版本优先从以下文件检测：

- Go：`go.mod`；
- Python：`pyproject.toml` 的 `requires-python`；
- Node：`package.json.engines.node`；
- Rust：`rust-toolchain.toml` 或 `rust-toolchain`。

无法确定时才使用语言默认版本。版本或 recipe 发生变化时创建新的 alias，不在仓库构建过程中临时升级旧模板。

### Repository Template

按以下键复用：

```text
(repo, base_commit, dependency_manifest_hash, repository_recipe_version)
```

Repository Template 从 Runtime Template 派生，负责：

- 复制指定 commit 的仓库内容；
- 联网安装仓库依赖；
- 执行必要的代码生成或前端构建；
- 编译测试目标；
- 保留离线运行测试所需的所有文件。

建议纳入依赖哈希的文件包括：

- Go：`go.mod`、`go.sum`；
- Python：`pyproject.toml`、`poetry.lock`、`uv.lock`、`requirements*.txt`；
- Node：`package.json`、`package-lock.json`、`pnpm-lock.yaml`、`yarn.lock`；
- Rust：`Cargo.toml`、`Cargo.lock`。

## E2B 构建伪代码

```python
from e2b import Template

def ensure_runtime_template(language: str, runtime_version: str) -> str:
    alias = runtime_alias(language, runtime_version, recipe_version="v1")
    if Template.alias_exists(alias):
        return alias

    dockerfile = render_runtime_dockerfile(
        language=language,
        runtime_version=runtime_version,
        install_time=True,
        install_build_tools=True,
    )
    builder = Template().from_dockerfile(dockerfile)
    info = Template.build(
        builder,
        alias=alias,
        cpu_count=2,
        memory_mb=4096,
        skip_cache=False,
    )
    return info.template_id


def build_repository_template(
    repo: dict,
    repo_path: str,
    runtime_template: str,
    base_commit: str,
) -> str:
    dependency_hash = hash_dependency_manifests(repo_path)
    alias = repository_alias(
        repo["full_name"],
        base_commit,
        dependency_hash,
        recipe_version="v1",
    )
    if Template.alias_exists(alias):
        return alias

    language = repo["language"].lower()
    builder = (
        Template(file_context_path=repo_path)
        .from_template(runtime_template)
        .set_workdir("/repo")
        .copy(".", "/repo")
        .run_cmd(REPOSITORY_BUILD_COMMANDS[language])
    )
    info = Template.build(
        builder,
        alias=alias,
        cpu_count=2,
        memory_mb=4096,
        skip_cache=False,
    )
    return info.template_id
```

## Stage 4：修订后的 H5 检验

真正的 H5 检验只负责确认已经准备好的 Repository Template 能否在断网环境中运行测试：

```python
from e2b import Sandbox

def verify_offline(template_id: str, test_cmd: str) -> dict:
    with Sandbox.create(
        template=template_id,
        allow_internet_access=False,
        timeout=600,
    ) as sandbox:
        result = sandbox.commands.run(test_cmd, timeout=600)
        return {
            "ok": result.exit_code == 0,
            "template_id": template_id,
            "reason": "ok" if result.exit_code == 0 else "offline_test_fail",
        }
```

建议将 H5 的语义明确为：

> 仓库依赖和编译产物经过一次联网准备后，完整测试套件可以在禁止联网的环境中稳定运行。

如果业务真正要求“从零开始也能离线安装依赖”，则需要另一项更严格的 vendor/cache 检验，不能与当前 H5 混用。

## 时间阈值口径

以下开销属于基础设施准备，不计入仓库 `build_timeout`：

- 拉取或导入基础镜像；
- 安装通用系统工具；
- 下载语言运行时或编译器；
- 构建、上传和注册 Runtime Template；
- 首次公共包代理缓存预热。

建议分别记录：

|指标|用途|是否用于淘汰仓库|
|---|---|---|
|`runtime_template_build_s`|观察基础设施健康度|否|
|`repository_template_build_s`|仓库依赖与编译成本观测|否，不设淘汰阈值|
|`offline_test_s`|H5 离线测试|是，建议阈值 600 秒|
|`sandbox_cold_start_s`|Stage 5 冷启动|是，阈值 20 秒|
|`benchmark_test_s`|Stage 5 测试耗时|是，阈值 120 秒|

基础设施构建失败应记录为 `infra_error` 或进入重试队列，不能写成仓库的 `build_fail`。

## Stage 5：Template 复用要求

Stage 5 必须复用通过 Stage 4 的同一个 Repository Template：

- 不重新安装依赖；
- 不重新编译仓库；
- 不重新注册另一个 template；
- `cold_start` 从调用 `Sandbox.create` 开始计时；
- Sandbox 设置 `allow_internet_access=False`；
- 三次运行使用同一 template ID。

这样测得的是实际任务执行开销，而不是环境构建开销。

## 建议的主流程

```python
def pipeline():
    for repo in candidates:
        hard_filter(repo)                                      # Stage 1
        score = soft_score(repo)                               # Stage 2
        direction = check_direction(repo)                      # Stage 3

        runtime_version = detect_runtime_version(repo)
        runtime_template = ensure_runtime_template(            # Stage 3.5
            repo["language"].lower(), runtime_version
        )
        repository_template = build_repository_template(
            repo, repo["workspace"], runtime_template, repo["base_commit"]
        )

        offline = verify_offline(                              # Stage 4
            repository_template,
            TEST_COMMANDS[repo["language"].lower()],
        )
        if not offline["ok"]:
            reject(repo, offline["reason"])
            continue

        benchmark_result = benchmark(                          # Stage 5
            repository_template,
            TEST_COMMANDS[repo["language"].lower()],
        )
        register(repo, direction, offline, benchmark_result, score)
```

## 本地 Docker 的定位

本地 Docker 路径可保留为：

- E2B 服务不可用时的 fallback；
- 调试 Runtime/Repository recipe；
- 对照验证 E2B 行为。

但使用本地 fallback 前也必须预拉基础镜像并准备工具链，不得把基础设施冷下载时间计入仓库判定。

本地 Docker 镜像不能直接被 E2B 远端构建器读取。若希望导入本地构建结果，必须先推送到 E2B 可访问的镜像仓库，再调用 `Template.from_image(image, username, password)`。

## 失败分类建议

|失败类型|归属|处理|
|---|---|---|
|基础镜像拉取失败|基础设施|`infra_error`，重试，不淘汰仓库|
|Runtime Template 构建失败|基础设施|`infra_error`，重试|
|E2B API 暂时不可用|基础设施|`infra_error`，重试|
|仓库依赖声明不可解析|仓库|`build_fail`|
|仓库专属 E2B Template 构建耗时较长|观测指标|继续等待完成，不淘汰|
|断网测试失败|仓库|`offline_test_fail`|
|Sandbox 冷启动超过 20 秒|仓库模板/执行成本|Stage 5 降级或淘汰|

## 合并进最终方案前需要确认

1. H5 是否定义为“联网准备后可断网运行”，还是“从零开始可离线安装”。
2. Repository Template 在线构建不设淘汰阈值（已确认）。
3. Runtime Template 的维护者、版本保留数量和过期清理策略。
4. E2B template 构建和存储成本预算。
5. `infra_error` 的最大重试次数与退避策略。
6. 是否保留本地 Docker 作为强制交叉验证，还是仅作为 fallback。

以上事项确认后，再统一修改《最终方案.md》的 H5 标准、Stage 4、Stage 5、Stage 6 登记字段和主流程，避免只修改局部而产生口径冲突。
