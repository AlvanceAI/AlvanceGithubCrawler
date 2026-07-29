Repository `bitnami/sealed-secrets` at commit `fb7da1e9ba98dfda0e068d6a3849ab2a40adc9d0` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 sealed-secrets controller 增加对带有 `sealedsecrets.bitnami.com/sealed-secrets-key=active` 标签的 Kubernetes Secret 的动态监听，在密钥 Secret 创建或更新时无需重启 Pod 即可重新加载并更新密钥注册表。
