新增 `validate-examples` 命令，将每个 Terraform 示例隔离到独立临时目录并注入默认 provider 配置，并行执行无 backend 的 `terraform validate`，汇总逐文件诊断后清理临时文件。
