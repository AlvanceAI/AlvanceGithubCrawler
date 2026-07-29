# 500 仓库生产管线运行手册

生产入口为 `scripts/run_production_pipeline.sh`。脚本默认完成以下流程：

1. 从五条语言查询各抽取 100 条原始记录，总样本固定为 500。
2. 对全部 500 条记录执行固定字段初筛；各语言不设通过配额。
3. 对所有初筛通过项执行软评分和方向核查，并写入可恢复的 E2B 队列。
4. 使用滚动窗口消费队列，一个任务结束后立即补位，最多保持 20 个在途任务。
5. 默认以 1 CPU / 1024 MB 完成离线测试、三次基准和 Harbor wrapper smoke。
6. 将明确的 OOM、离线超时和基准资源失败项统一重排队一次，以 2 CPU / 4096 MB
   重新验证。资源规格会进入 E2B alias，不能误复用 1/1 模板。
7. 生成 task、material、catalog 记录，以及本次运行的 JSON/Markdown 统计文件。

## 首次运行

选择一个稳定且唯一的 `PIPELINE_RUN_ID`。后续恢复必须继续使用同一个值：

```bash
PIPELINE_RUN_ID=github-500-20260729 \
  scripts/run_production_pipeline.sh
```

脚本会从仓库根目录的 `.env` 读取凭据。不要把 API key 写进命令行或日志。

## 恢复运行

抓取、初筛和 pending 队列都是可恢复的。同一运行中断后，原命令再次执行即可：

```bash
PIPELINE_RUN_ID=github-500-20260729 \
  scripts/run_production_pipeline.sh
```

默认最多执行 5 轮临时错误重试。若仍有基础设施错误，脚本以退出码 3 结束并保留
现场；增加轮数时仍使用相同 `RUN_ID`：

```bash
PIPELINE_RUN_ID=github-500-20260729 VERIFY_ROUNDS=8 \
  scripts/run_production_pipeline.sh
```

## 并发与资源

- `E2B_CONCURRENCY` 默认 20，脚本拒绝大于免费账户上限 20 的值。
- 默认资源固定为 1 CPU / 1024 MB。
- 只有 `e2b_resource_exhausted`、`benchmark_resource_fail` 和
  `offline_test_timeout` 会进入一次 2 CPU / 4096 MB 升级阶段。
- 资源升级阶段有独立 checkpoint，恢复运行不会重复重排队已处理项目。

排障时可以临时降低并发，但正式生产运行应保留默认值 20：

```bash
PIPELINE_RUN_ID=github-500-debug E2B_CONCURRENCY=4 \
  scripts/run_production_pipeline.sh
```

## 输出与日志

默认运行目录为 `outputs/production-runs/<RUN_ID>/`：

```text
outputs/production-runs/<RUN_ID>/
├── crawl/                  # 500 条原始记录、初筛结果和 crawl checkpoint
├── production/             # pending、candidates、rejections 总账
├── logs/                   # 每个阶段、每轮验证的完整 stdout/stderr
├── stage-timings.jsonl     # 阶段起止时间、耗时和退出码
├── metrics.json            # 机器可读漏斗、语言、资源和性能统计
└── statistics.md           # 可继续整理为最终交付文档的统计草稿
```

`statistics.md` 会列出抓取/初筛/E2B/task 漏斗、每种语言的自然通过数量、每阶段耗时，
以及每个最终 task 的冷启动、测试中位数、峰值内存和资源规格。原始日志始终保留，方便
后续追查长尾项目和重新计算指标。

可通过以下变量调整目录，不影响恢复语义：

```bash
PIPELINE_RUN_ROOT=/data/alvance-runs \
PIPELINE_RUN_ID=github-500-20260729 \
  scripts/run_production_pipeline.sh
```

## 完整性判断

一次运行只有同时满足以下条件才标记为 `complete`：

- crawl summary 为 `completed`；
- pending remaining 为 0；
- 每条 candidate 已完成 E2B 离线测试、三次基准和 wrapper smoke；
- candidate 已生成对应 task、material 和 catalog 记录。

脚本退出后先查看 `metrics.json` 的 `status` 和 `pending_remaining`，再使用
`statistics.md` 编写最终按语言分类的交付文档。

## 双 Key 持续量产

当 `.env` 同时提供 `E2B_API_KEY1` 和 `E2B_API_KEY2` 时，使用持续量产入口：

```bash
PIPELINE_RUN_ID=github-mass-production-20260729 \
  scripts/run_continuous_production.sh
```

`PIPELINE_E2B_CONCURRENCY`/`E2B_CONCURRENCY` 表示每个 Key 的并发数，默认每个 Key
20，总并发 40。脚本复用现有 crawl 和 production checkpoint，逐批把样本扩展到
每种语言 1000 条（GitHub Search 单查询上限），生产者与 E2B 消费者并行运行。每轮完整
task 会自动提交并推送到 `XBY`；原始日志、阶段耗时、最终指标和 Markdown 统计保存在
`outputs/production-runs/<RUN_ID>/`。

任一 Key 额度耗尽后，其未完成任务会转交另一 Key；两个 Key 都耗尽时脚本以退出码 4
停止并保留 pending checkpoint。日志只显示 Key 槽编号，不包含密钥值。
