为 get-token 增加可选的客户端证书与私钥文件参数，并将其读取、编码后写入 ExecCredential 输出的 status.clientCertificateData 和 status.clientKeyData 字段，以支持通过 mTLS 反向代理访问 Kubernetes API。
