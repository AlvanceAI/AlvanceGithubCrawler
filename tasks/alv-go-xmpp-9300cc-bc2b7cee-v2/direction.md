重构连接管理流程，使管理器仅对支持 XMPP Stream Management 的客户端调用 Resume，组件及不支持流管理的客户端直接执行 Connect。
