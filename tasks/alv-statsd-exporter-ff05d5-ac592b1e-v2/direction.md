新增受生命周期配置控制的 `/-/clear` HTTP 端点，原子清除已积累的 StatsD 指标注册状态，同时保留 Go 运行时及 exporter 自监控指标并继续接收新指标。
