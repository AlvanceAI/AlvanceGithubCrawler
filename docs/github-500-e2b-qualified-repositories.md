# GitHub 500 仓库 E2B 最终结果

- 状态：`complete`
- 生成时间：`2026-07-29T12:54:00Z`
- 原始样本：500 个 GitHub 仓库，每条语言查询取 100 个仅用于构成样本
- 筛选口径：初筛、评分、方向核查和 E2B 阶段均未设置语言配额
- E2B：默认 `1 CPU / 1024 MB`，资源失败项升级为 `2 CPU / 4096 MB`；滚动并发上限 20
- 最终结果：6 个可交付 task，5 个稳定、1 个按管线策略标记为 flaky，pending 为 0

## 筛选漏斗

| 语言 | 原始样本 | 固定字段初筛通过 | 进入 E2B | 最终 task |
|---|---:|---:|---:|---:|
| Python | 100 | 54 | 14 | 2 |
| Go | 100 | 65 | 22 | 3 |
| TypeScript | 100 | 35 | 4 | 0 |
| JavaScript | 100 | 33 | 8 | 1 |
| Rust | 100 | 52 | 11 | 0 |
| **合计** | **500** | **239** | **59** | **6** |

账目已闭合：初筛通过的 239 个仓库等于 6 个最终候选加 233 个最终拒绝；59 个
E2B 项均已有终态。初筛淘汰 261 个，Stage 2/3 淘汰 180 个，E2B 淘汰 53 个。

## Go

| 仓库 | 精确 commit | 许可证 | Stars | 分数（调整后/原始） | 资源与测试命令 | 冷启动/测试/峰值内存 | Flaky | Task |
|---|---|---|---:|---:|---|---|---|---|
| [bitnami/sealed-secrets](https://github.com/bitnami/sealed-secrets) | [fb7da1e9ba98dfda0e068d6a3849ab2a40adc9d0](https://github.com/bitnami/sealed-secrets/commit/fb7da1e9ba98dfda0e068d6a3849ab2a40adc9d0) | Apache-2.0 | 9,221 | 10/10 | `1 CPU / 1024 MB`; `go test ./...` | 0.45s / 106.06s / 744.1MB | 否 | [alv-sealed-secrets-2ab4a1-fb7da1e9-v2](../tasks/alv-sealed-secrets-2ab4a1-fb7da1e9-v2) |
| [hetznercloud/hcloud-cloud-controller-manager](https://github.com/hetznercloud/hcloud-cloud-controller-manager) | [27253f52c336e71fcac8441845ab0ff6e418ce60](https://github.com/hetznercloud/hcloud-cloud-controller-manager/commit/27253f52c336e71fcac8441845ab0ff6e418ce60) | Apache-2.0 | 921 | 8/8 | `1 CPU / 1024 MB`; `go test ./...` | 0.48s / 91.86s / 665.8MB | 否 | [alv-hcloud-cloud-control-a2a07e-27253f52-v2](../tasks/alv-hcloud-cloud-control-a2a07e-27253f52-v2) |
| [kube-vip/kube-vip](https://github.com/kube-vip/kube-vip) | [0d248ba40fd7004050f258b615ed6cfceac932b6](https://github.com/kube-vip/kube-vip/commit/0d248ba40fd7004050f258b615ed6cfceac932b6) | Apache-2.0 | 2,914 | 10/10 | `1 CPU / 1024 MB`; offline `go test ./...`; benchmark `go test ./pkg/bgp/...` | 0.39s / 27.91s / 144.5MB | 否 | [alv-kube-vip-51d2e4-0d248ba4-v2](../tasks/alv-kube-vip-51d2e4-0d248ba4-v2) |

## Python

| 仓库 | 精确 commit | 许可证 | Stars | 分数（调整后/原始） | 资源与测试命令 | 冷启动/测试/峰值内存 | Flaky | Task |
|---|---|---|---:|---:|---|---|---|---|
| [NSPC911/rovr](https://github.com/NSPC911/rovr) | [e800285910913db9a3afc2bc53a846fa64b0c747](https://github.com/NSPC911/rovr/commit/e800285910913db9a3afc2bc53a846fa64b0c747) | MIT | 389 | 9/9 | `1 CPU / 1024 MB`; `python -m pytest -x -q` | 0.42s / 37.47s / 308.3MB | 否 | [alv-rovr-462fd8-e8002859-v2](../tasks/alv-rovr-462fd8-e8002859-v2) |
| [zhnt/loushang](https://github.com/zhnt/loushang) | [7ed49fc9b26efcc2d42a6ee1f163c042f4b7e55f](https://github.com/zhnt/loushang/commit/7ed49fc9b26efcc2d42a6ee1f163c042f4b7e55f) | Apache-2.0 | 895 | 7/9 | `1 CPU / 1024 MB`; `python -m pytest -x -q` | 0.63s / 67.07s / 196.3MB | 是 | [alv-loushang-2b9ea9-7ed49fc9-v2](../tasks/alv-loushang-2b9ea9-7ed49fc9-v2) |

`zhnt/loushang` 通过断网测试，但三次基准未全部通过；管线按 flaky 规则扣 2 分后
仍达到阈值，因此保留并显式标记。下游若只接受稳定套件，应排除这一项。

## JavaScript

| 仓库 | 精确 commit | 许可证 | Stars | 分数（调整后/原始） | 资源与测试命令 | 冷启动/测试/峰值内存 | Flaky | Task |
|---|---|---|---:|---:|---|---|---|---|
| [devswha/patina](https://github.com/devswha/patina) | [b98b3b03e885e6996750d88f7b851010be6ed912](https://github.com/devswha/patina/commit/b98b3b03e885e6996750d88f7b851010be6ed912) | MIT | 276 | 9/9 | `1 CPU / 1024 MB`; `CI=1 npm test` | 0.49s / 118.28s / 101.1MB | 否 | [alv-patina-6b5b94-b98b3b03-v2](../tasks/alv-patina-6b5b94-b98b3b03-v2) |

TypeScript 和 Rust 本轮没有最终通过项。

## 资源升级结果

7 个疑似资源不足项进入 `2 CPU / 4096 MB` 阶段，没有新增最终 task：3 个暴露为
确定性测试失败，2 个仍超过 600 秒离线测试上限，1 个未通过基准资源阈值，
`rustfs/rustfs` 在 4GB 下构建仍被 SIGKILL。

## 性能与日志

| 已记录阶段 | 墙钟耗时 | 说明 |
|---|---:|---|
| GitHub 抓取与固定字段初筛 | 344.19s | 500 个样本，834 次 GitHub API 请求 |
| 默认资源恢复验证 | 760s | 收口最后 2 个默认资源 pending |
| 2核/4GB 并行预构建 | 1,307s | 7 个模板并行，6 个就绪、1 个 SIGKILL |
| 2核/4GB 正式验证 | 798s | 6 个项目在同一秒启动，并发上限仍为 20 |
| Rust 失败缓存恢复与最终重建 | 541s | 修复不可启动 alias 误命中后完成终态记录 |
| 端到端观测窗口 | 13,243s | 09:08:23 至 12:49:06，包含恢复间隔与并行重叠 |

初始大批量 E2B 阶段在恢复前未保存独立 stdout 日志，因此未虚构该阶段耗时；其
逐项时间和终态仍保存在 `pending.jsonl`、`rejections.jsonl` 和 `candidates.jsonl`。

完整运行数据位于 [outputs/github_production_500_unquota](../outputs/github_production_500_unquota)，
阶段日志位于 [logs](../outputs/github_production_500_unquota/logs)，机器可读汇总为
[metrics.json](../outputs/github_production_500_unquota/metrics.json)。6 个候选均已核验：task、
material、catalog 记录齐全且 commit/资源一致，Harbor wrapper smoke 全部成功。
