实现显式启用的 Unix 域套接字控制通道，以 NDJSON 接收并反序列化 UserIntent，将其作为 AppEvent 注入现有事件循环，并保证错误隔离、套接字权限及退出清理。
