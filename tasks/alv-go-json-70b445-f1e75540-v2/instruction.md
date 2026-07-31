Repository `goccy/go-json` at commit `f1e7554014296f3d97b2367c524a14b3b8877ab6` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

重构流式 Decoder.Token 的缓冲区回收与转义字符串解析，使扫描大型 JSON 文件时保持有界内存并避免重复拷贝导致的性能退化。
