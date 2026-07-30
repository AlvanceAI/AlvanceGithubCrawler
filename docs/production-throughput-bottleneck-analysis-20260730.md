# 生产管线吞吐瓶颈与优化预估

> 快照时间：`2026-07-30 08:37:48 UTC`。本分析只读日志、队列和产物；生产进程没有暂停。数值会随管线继续运行而变化。

## 结论

当前第一瓶颈是**预筛给 E2B 供料的速度和稳定性**，不是 E2B Key 数量或 E2B 并发配置。

当前已配置 3 个 E2B Key，每个 20 并发，共 60 个验证槽位。但本轮实际观测到的最高 E2B 在途数只有 33；快照时队列只剩 5 个活动项，最后一条验证日志的在途数已降到 2。E2B 长时间在等候选仓库，因此再增加 E2B 并发不会带来线性提升。

当前保守产出约为 **38 个可交付 Task/小时**。先修复模型网关不稳定和预筛供料后，合理的近期目标是 **70-80 Task/小时**；继续消除重复 GitHub 请求并改成流水线生产后，目标区间是 **105-145 Task/小时**。这两个数字都是基于本次实测通过率的容量推算，必须在优化后连续运行至少两小时复测确认。

## 快照数据

| 指标 | 实测值 | 含义 |
|---|---:|---|
| 本轮启动时间 | `07:38:32 UTC` | 当前连续生产实例 |
| 快照前新增可交付 Task | 37 | 从 `candidates.jsonl` 的 `registered_at` 统计 |
| 保守 Task 吞吐 | 约 38/h | 37 个 Task / 59 分 16 秒，包含启动和排空影响 |
| E2B 完成事件 | 142 | 37 registered、99 rejected、4 error_exhausted、2 already_registered |
| 本轮 E2B 注册率 | 26.1% | 37 / 142；用于下方容量估算 |
| E2B 槽位 | 60 | 3 Key x 20；由当前脚本和配置提供 |
| 已观测最高 E2B 在途 | 33 | 小于 60，说明没有被候选队列喂满 |
| 快照时活动 pending | 5 | 无法维持满载 |
| E2B 单次尝试耗时 | 平均 283.7s，P50 168.9s，P90 701.4s | 143 次从提交到完成的日志配对；长尾明显 |

本轮成功 Task 的阶段数据也说明，E2B 本身不是当前第一堵点。37 个成功样本中，仓库模板构建平均 112.9 秒，离线测试平均 35.7 秒，三次 benchmark 的单次中位测试平均 26.6 秒，wrapper 构建平均 12.0 秒；运行时模板命中 34/37，但仓库模板命中 0/37。仓库各不相同，仓库模板无法跨项目复用是预期行为。

## 为什么是预筛

当前路径为：

```text
GitHub crawl -> prescreen -> pending queue -> E2B verify -> Task/material/catalog
```

已完成的 13 个预筛批次总共入队 688 个候选，累计耗时 9,580 秒，折合 **258.6 个候选/小时**。剔除两个明显异常缓慢批次后，健康供料约 **307.6 个候选/小时**；历史最好批次为 **410.1 个候选/小时**。这仍然远低于填满 60 个 E2B 槽位所需的约 760 个候选/小时。

最明显的异常是 `prescreen-9500`：129 个待处理候选只入队 33 个，耗时 1,063 秒，即 **111.8 个候选/小时**。该批次记录了 74 次 `direction judge retry`，主要是 502、超时和限流。相比之下，`prescreen-resume-9000` 在 548 秒内入队 41 个，约 269.3 个候选/小时。

换句话说，E2B 的 60 个工位已经准备好，但上游每小时只稳定送来约 260-310 个合格候选，而且还会因模型重试出现长时间断供。

## 主要瓶颈

| 优先级 | 瓶颈 | 证据 | 影响 |
|---|---|---|---|
| P0 | 模型网关重试和共享退避 | `prescreen-9500` 有 74 次重试；一次 502 可触发 60 秒退避 | 20 个预筛线程一起被拖慢，E2B 队列见底 |
| P1 | GitHub 请求被全局锁串行化 | [github.py](../src/alvance_github_crawler/github.py#L74) 在整个 HTTP 请求期间持有 `_request_lock` | 20 个预筛线程的 GitHub 调用实际一次只能飞一个 |
| P1 | 已爬取快照又重复取 GitHub 元数据、commit tree 和完整 tree | crawl 已取得 `base_commit`、`source_tree`、`file_count`、测试证据；[pipeline.py](../src/alvance_github_crawler/pipeline.py#L278) 仍重新请求 repository、commit tree 和 tree | 每个候选增加多次网络请求和等待 |
| P1 | Feature issue 重复查询 | [scoring.py](../src/alvance_github_crawler/screening/scoring.py#L193) 调一次，随后 [direction.py](../src/alvance_github_crawler/screening/direction.py#L287) 再调一次 | 同一仓库重复访问 issue API，放大 GitHub 串行瓶颈 |
| P1 | producer 内部按 crawl 后 prescreen 的串行批次运行 | [run_continuous_production.sh](../scripts/run_continuous_production.sh#L175) | crawl 期间不会持续为 pending 队列供料，造成 E2B 空转 |
| P2 | 失败候选占用 E2B 很久 | 被拒尝试平均 314.5 秒，成功尝试平均 250.5 秒；本轮有 24 个 `e2b_resource_exhausted` | 在 E2B 被喂满之后才会成为显著吞吐瓶颈 |
| P3 | JSONL 队列每次入队重放全文件 | [queue.py](../src/alvance_github_crawler/pending/queue.py#L41) 的 `enqueue()` 调用 `pending()`；当前文件约 2.5 MB | 候选量继续增长后出现 O(N^2) 读放大，但暂不是第一问题 |

### 模型退避为什么会放大

[direction.py](../src/alvance_github_crawler/screening/direction.py#L107) 让所有线程共享下一次模型请求时间。某个请求遇到 502/超时后，[同文件](../src/alvance_github_crawler/screening/direction.py#L116) 会把这个共享时间推迟。这个设计避免每个线程独立重试风暴，但在网关报 `retry_after=60` 时，会使后续所有仓库一起停顿，形成“20 线程看起来开着，实际都在等”的状态。

### 为什么不能简单删除二次校验

现有 crawl 快照缺少 `size`，而 hard filter 仍依赖完整 tree 来确认测试基础设施。因此不应直接把二次请求删掉。正确做法是把 `size` 和 hard-filter 所需的紧凑 tree/test 快照一起写入 crawl 记录，或者在 crawl 阶段完成 hard filter；之后 prescreen 复用这个固定快照，并在本地 clone 时校验 `base_commit`/`source_tree`。这样既保留固定提交的可追溯性，也避免重复网络读取。

## 优化后的提升预估

下表使用本轮 26.1% 注册率计算，同时给出保守范围。它是容量模型，不是承诺产量。

| 方案 | 候选供给假设 | 预估可交付 Task/h | 相对当前约 38/h |
|---|---:|---:|---:|
| 当前实测基线 | 队列经常排空 | 约 38 | 1.0x |
| 只稳定模型网关与重试 | 恢复到健康供料 308/h | 70-80 | 1.8-2.1x |
| 再去除重复 GitHub 请求并改流水线 | 目标供料 450-550/h | 105-145 | 2.8-3.8x |
| E2B 理论满载 | 60 x 3,600 / 283.7 = 761 次验证/h | 175-200 | 4.6-5.3x |

最后一行需要持续约 760 个候选/小时，远高于当前预筛能力，也会受 GitHub Code Search 与模型服务额度约束。因此它是硬件/服务上限，不是下一步交付目标。

## 建议的实施顺序

1. 先补指标：记录每阶段耗时、候选入队率、pending 深度、每个 Key 的在途数、模型错误码及 GitHub API 资源类型。没有这些指标，优化后无法证明提升来自哪里。

2. 修复模型供料：模型调用改为自适应并发，初始建议 6-8 个在途模型请求；按错误率降档，成功窗口后缓慢升档；对连续 502 建立熔断和备用 endpoint/model。保留有界重试，但不要让单个 60 秒退避阻塞所有新请求。

3. 修复 GitHub 并发：使用线程本地 `requests.Session`；锁只保护速率计数、配额和短暂的时间戳更新，不要包住网络请求；核心 API 与 Code Search 分别限速。

4. 复用 crawl 固定快照：在 crawl 记录增加 `size` 和 hard-filter 所需信息，消除 prescreen 的 repository/commit/tree 重取；Feature issue 只取一次并在 score 与 direction 之间共享。

5. 改为真正流水线：crawl、prescreen 和 E2B 同时工作，按增量记录投递，不等一整个 500 条 batch 完成再进入下一阶段。设置至少 120 个 pending 的缓冲水位，低于水位时优先补料。

6. 最后才处理 E2B 长尾：预判大内存/大依赖项目，仍然先用 1 CPU/1 GB；仅对资源失败项转 2 CPU/4 GB。不要把全部仓库升级规格，这会更快消耗额度且不能解决缺料。

7. 当队列增长到数千项后，把 append-only JSONL 队列替换为 SQLite 或保留内存索引，避免每次入队全量重放。

## 验收标准

优化不以“线程数更高”为完成标准，而以以下连续两小时窗口为准：

- pending 大多数时间维持在 120 以上，E2B 在途数稳定接近 54/60；
- 模型重试率和 60 秒全局退避次数显著下降；
- 预筛稳定入队至少 300 个候选/小时，随后争取 450 个/小时；
- 可交付 Task 稳定超过 70 个/小时后，再判断是否继续追求 100+ 个/小时；
- 固定 `base_commit`、`source_tree`、Dockerfile/material 和 E2B template provenance 仍完整保留。

## 数据来源

- `outputs/production-runs/github-mass-production-XBY-20260730/logs/`
- `outputs/production-runs/github-mass-production-XBY-20260730/stage-timings.jsonl`
- `outputs/github_production_500_unquota/candidates.jsonl`
- `outputs/github_production_500_unquota/pending.jsonl`
- `outputs/github_production_500_unquota/rejections.jsonl`
