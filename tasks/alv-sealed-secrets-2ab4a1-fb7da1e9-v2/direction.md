为 sealed-secrets controller 增加对带有 `sealedsecrets.bitnami.com/sealed-secrets-key=active` 标签的 Kubernetes Secret 的动态监听，在密钥 Secret 创建或更新时无需重启 Pod 即可重新加载并更新密钥注册表。
