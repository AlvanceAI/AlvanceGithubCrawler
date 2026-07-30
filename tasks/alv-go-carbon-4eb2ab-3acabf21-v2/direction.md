实现启动时检测存储 schema 与聚合配置变更，并主动扫描、迁移所有已有 Whisper 文件，使长期无写入的 stale metrics 也更新到当前保留策略和聚合规则。
