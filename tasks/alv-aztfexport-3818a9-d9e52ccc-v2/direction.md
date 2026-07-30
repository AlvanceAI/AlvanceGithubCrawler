在 Terraform 模式下检测 Terraform 版本及目标 Provider 对 `GenerateResourceConfig` RPC 的支持情况，满足条件时用该 RPC 生成精确资源配置，否则回退到 `tfadd`。
