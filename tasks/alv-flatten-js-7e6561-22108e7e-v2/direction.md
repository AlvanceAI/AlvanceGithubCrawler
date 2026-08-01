重构 Multiline.split，使其按单个点非破坏性地切分并返回与 Segment、Arc、Line 一致的两部分结果（单一图形不额外包装），同时保留原有批量切边能力为 splitEdges，并正确处理包含 Ray 的多线段。
