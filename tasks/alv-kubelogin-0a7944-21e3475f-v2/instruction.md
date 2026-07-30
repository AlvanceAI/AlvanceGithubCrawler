Repository `int128/kubelogin` at commit `21e3475f3922cfcbdbcef7c3b464a2fb38cbea73` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 get-token 增加可选的客户端证书与私钥文件参数，并将其读取、编码后写入 ExecCredential 输出的 status.clientCertificateData 和 status.clientKeyData 字段，以支持通过 mTLS 反向代理访问 Kubernetes API。
