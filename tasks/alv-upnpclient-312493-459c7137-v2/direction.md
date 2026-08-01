为 Device 和 discover() 增加可配置的 TLS 证书校验选项，并通过共享 requests.Session 将该配置一致应用于设备描述、SCPD、SOAP 等所有 HTTP 请求，以支持使用自签名证书的 UPnP 设备。
