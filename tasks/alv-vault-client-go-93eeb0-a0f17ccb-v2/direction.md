实现一个可跨语言复用的 OpenAPI 预处理过滤器，从外部排除列表读取 operationId，在调用 openapi-generator 前删除匹配的 API 操作，并以测试验证流式、废弃及编号重复端点不会进入生成库。
