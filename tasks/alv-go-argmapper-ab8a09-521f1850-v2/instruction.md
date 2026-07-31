Repository `hashicorp/go-argmapper` at commit `521f1850288386fa7276aff66bab2fa289ec80e6` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

新增 `FromStruct` 参数适配器，通过反射读取传入结构体的导出字段及标签，并将其展开为可供依赖注入匹配的 `Named`／`Typed` 参数。
