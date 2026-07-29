Repository `vouchdev/vouch` at commit `302363ca56246e093e9334488399005e05b5b977` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为现有检索管线增加只读的 `kb.explain_ranking` 调试接口，在不复制评分逻辑且遵守 `kb.context` viewer scope 的前提下，返回候选结果的融合评分、可选重排与时效信号及过滤门控决策，并通过 MCP、JSONL 和 CLI 暴露。
