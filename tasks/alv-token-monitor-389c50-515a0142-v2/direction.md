优化 Hub 实时同步协议：对无实质变化的 ingest 跳过或合并广播，SSE 仅下发轻量统计并将 session/project 明细改为按需获取，同时让 ingest 默认返回精简确认。
