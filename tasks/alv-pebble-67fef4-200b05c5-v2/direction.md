为 Pebble ACME 测试服务器增加可配置的随机限流机制，按指定比例拒绝请求并返回 acme:error:rateLimited，且尽可能附带 Retry-After 响应头。
