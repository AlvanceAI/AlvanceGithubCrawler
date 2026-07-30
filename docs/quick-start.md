# 运行、配置与初步测试

## 结论

项目要求 Python 3.11+，并从项目根目录运行。当前主机已有 `.env`，三项凭据均已通过
真实接口验证（检查日期：2026-07-29）。项目环境由 `uv` 管理；Docker CLI 已安装，但
当前用户无权访问 `/var/run/docker.sock`；`gh` 未安装。

本次凭据验证结果：

- GitHub：公开仓库读取和 Code Search 成功，认证额度为 5,000 次/小时；
- LLM：`gpt-5.6-sol` 的 Responses API 结构化输出成功；
- E2B：成功创建临时 Sandbox、执行命令并销毁。

最小可行测试需要：

- GitHub 凭据：`GITHUB_TOKEN`，或已经登录的 `gh auth`；
- 模型凭据：`OPENAI_API_KEY`；
- 联网能力：访问 GitHub、模型接口、grep.app/Sourcegraph 和依赖源；
- 本地离线验证还需要可用的 Docker daemon；
- 完整 E2B 流程另需 `E2B_API_KEY`。

## 需要填写的配置

先执行 `cp .env.example .env`，再填写 `.env`。不要提交该文件。

```dotenv
# 必填；只爬公开仓库时使用只读 fine-grained PAT 即可
GITHUB_TOKEN=

# 必填；Stage 3 用模型分析 GitHub feature issue
OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_MODEL=gpt-5-mini

# 单 Key 命令的 E2B 凭据；双 Key 持续量产时使用下面的编号配置
E2B_API_KEY=
E2B_API_KEY1=
E2B_API_KEY2=

PIPELINE_E2B_CONCURRENCY=20
PIPELINE_PRESCREEN_CONCURRENCY=20

# 可选；建议每轮试跑使用独立目录
PIPELINE_OUTPUT_DIR=output/test-1
```

使用 OpenAI 官方接口时，`OPENAI_BASE_URL` 留空。使用兼容网关时填写网关地址，且网关
必须支持 Responses API、结构化输出以及所选模型。项目也接受 `MODEL_API_KEY`、
`MODEL_BASE_URL`、`MODEL_NAME` 和 `E2B_KEY` 这些别名。

## GitHub 是否需要 Key

对这个项目而言需要。代码在启动主流程时会校验 `GITHUB_TOKEN`；若未填写，只会尝试
读取 `gh auth token`。当前主机没有 `gh`，因此现在必须填写 `GITHUB_TOKEN`（或先安装
并登录 GitHub CLI）。项目只读取公开仓库时无需写权限，也不要授予私有仓库权限。

Key 的影响很大：

| 场景 | 常见限制 | 对本项目的影响 |
| --- | --- | --- |
| 未认证 REST API | 每个 IP 通常 60 次/小时；Search 通常 10 次/分钟 | tree、commit、contents、issues 等请求很快耗尽额度 |
| PAT/`gh auth` 认证 | REST API 通常 5,000 次/小时；Search 通常 30 次/分钟 | 适合小批量和持续爬取 |
| GitHub Code Search | 要求认证，通常 10 次/分钟 | Stage 3 的重复实现检查依赖它，无认证无法完成主流程 |

以上是 GitHub 公共 REST API 的常见默认值，GitHub App、企业账号和平台策略可能不同。
限流说明见 [REST API 限流](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api)
和 [Search API](https://docs.github.com/rest/search/search)。

## 安装

当前项目使用 `uv` 创建和管理 `.venv`，不需要手动创建或激活虚拟环境。

```bash
uv sync --extra e2b --extra dev
cp .env.example .env
```

若暂时完全不使用 E2B，也可执行 `uv sync --extra dev`。后续命令使用 `uv run`，例如
`uv run alvance-github-crawler --doctor` 和 `uv run pytest`。

先修复 Docker 使用权限并确认 daemon 已启动；爬虫会直接调用 `docker`，所以仅能通过
`sudo docker` 运行仍不够。当前主机可执行：

```bash
sudo usermod -aG docker "$USER"
# 退出并重新登录后执行
docker info
```

Docker 组具有接近 root 的权限，只应为可信用户配置。

## 建议的测试顺序

1. 检查配置和本机工具：

   ```bash
   alvance-github-crawler --doctor
   pytest
   ```

   `--doctor` 输出中的 Key 应为 `true`，工具路径也应正常。它不会联网验证 Key 是否有效，
   也不会检查 Docker daemon 权限。

2. 只测试 GitHub、模型分析和候选入队，不使用 Docker/E2B：

   ```bash
   alvance-github-crawler --defer-e2b --max-repos 1 --verbose
   ```

3. Docker 可用后，执行一次本地离线验证：

   ```bash
   alvance-github-crawler --skip-e2b --max-repos 1 --verbose
   ```

   此模式结果为 `offline_verified_local`，不等同于完整 E2B 结果。

4. 填好 `E2B_API_KEY` 后执行完整流程：

   ```bash
   alvance-github-crawler --max-repos 1 --verbose
   # 或消费第 2 步产生的队列
   alvance-github-crawler --verify-pending --max-repos 1 --verbose
   ```

持续双 Key 量产必须切换到 `XBY` 分支，并填写 `E2B_API_KEY1`、`E2B_API_KEY2`：

```bash
git switch XBY
./run.sh
```

`--max-repos 1` 表示只处理一个搜索结果，该仓库可能在筛选阶段被拒绝，因此没有候选产物
并不一定表示运行失败。确认链路正常后再逐步增大数量，避免 GitHub/模型限流以及 E2B 费用。

## 输出位置

按上面的配置，运行状态写入 `output/test-1/` 下的 `candidates.jsonl`、
`rejections.jsonl` 和 `pending.jsonl`。成功的完整流程还会更新 `catalog/`、`materials/`
和 `tasks/`。状态采用追加写入，同一仓库后续默认会跳过；重新试验时优先换一个新的
`PIPELINE_OUTPUT_DIR`，不要混用不同测试轮次的数据。
