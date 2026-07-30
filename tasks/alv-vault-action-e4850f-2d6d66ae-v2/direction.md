扩展 secrets DSL 的解析与导出逻辑，允许为单个 Vault secret 值指定 masked=false，从而跳过 GitHub Actions 的日志掩码注册，同时保持默认值仍被掩码。
