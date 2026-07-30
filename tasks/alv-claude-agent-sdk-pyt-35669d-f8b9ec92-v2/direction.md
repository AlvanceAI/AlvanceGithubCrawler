为持久化 ClaudeSDKClient 增加逐次 query 的 W3C trace context 捕获与控制协议传播，使每轮 MCP/工具调用归属当前调用方 trace，而非进程启动时的 trace。
