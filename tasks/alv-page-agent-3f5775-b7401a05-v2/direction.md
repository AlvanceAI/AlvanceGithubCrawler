为 PageAgent 核心 API 增加可持续复用会话上下文的多轮对话机制，使后续消息追加到当前 agent thread，并仅在显式请求时创建新任务。
