Repository `lovasoa/marshmallow_dataclass` at commit `5c428f493ef3059246974bedf9a7d89599994b34` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

修复从泛型基类继承的 dataclass 在生成 Marshmallow schema 时未解析具体类型参数、导致对 TypeVar 调用 issubclass 引发 TypeError 的问题。
