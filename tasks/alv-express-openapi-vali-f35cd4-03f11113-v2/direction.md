扩展响应验证中间件，使其拦截 Express 的 `res.send()` 并对图片、二进制及其他非 JSON 响应的 Content-Type 和响应体执行 OpenAPI 校验。
