Repository `SSLMate/go-pkcs12` at commit `c0472edb16891765fbc86573ea468365b7fd2197` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

实现 DecodeChains API，解析包含多个私钥包的 PKCS#12 数据，按 FriendlyName 和密钥对应关系匹配叶证书，并递归构建各自的 CA 证书链。
