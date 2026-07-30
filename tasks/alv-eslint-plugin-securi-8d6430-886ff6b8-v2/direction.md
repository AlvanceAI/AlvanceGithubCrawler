为 security/detect-non-literal-regexp 规则增加对 RegExp.escape 包裹动态正则内容的安全识别，并提供将可修复动态插值自动包裹为 RegExp.escape(...) 的 autofix。
