重构 Signalbot API：以统一的 Pydantic Message 模型解析所有收发消息，使发送、编辑、远程删除和反应等操作统一接收并返回 Message，同时封装附件的 Base64 编解码细节。
