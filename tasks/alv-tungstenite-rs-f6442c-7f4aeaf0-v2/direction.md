为服务端握手新增可定制错误处理的 accept API，使调用方能在缺少 Upgrade、Connection 等 WebSocket 头时返回有效 HTTP 错误响应，而不是直接丢弃底层流。
