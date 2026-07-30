重构 XML feed 的字符集处理链路：先通过 BOM、XML 声明及内容嗅探将输入统一解码为 UTF-8，再按 rune 清理无效 UTF-8、U+FFFE/U+FFFF 等非法字符后交给 Atom/RSS 解析器。
