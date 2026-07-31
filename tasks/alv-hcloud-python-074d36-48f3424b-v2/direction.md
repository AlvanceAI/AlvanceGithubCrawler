将 SDK 的底层 HTTP 传输从 requests/urllib3 迁移到支持 HTTP/2 的客户端，并在保持现有公开 API、认证、超时、重试和错误处理语义的前提下默认通过 HTTP/2 请求 Hetzner Cloud API。
