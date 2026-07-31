让 Rune 工作负载中的 `execute` 和 `execute_prepared` 返回可检查的 Cassandra 查询结果，而非始终返回 unit，以便脚本验证空结果或字段值并主动判定工作负载失败。
