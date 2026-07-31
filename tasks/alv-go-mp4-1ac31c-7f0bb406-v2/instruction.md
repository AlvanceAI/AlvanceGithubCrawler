Repository `abema/go-mp4` at commit `7f0bb4060772e78fb52d48b73a38b8c3928e83f0` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

移除 MP4 字段解析中的 `string=c_p` 标签及其依赖 `Seek` 的 `unmarshalString_C_P` 逻辑，并将定长填充字符串的读取迁移到 `OnReadField` 处理器。
