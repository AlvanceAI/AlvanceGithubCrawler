Repository `Kludex/starlette` at commit `5174d4c8358a6f06aa8056bafd14c2272dab8dd1` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 TestClient 实现真正的流式响应传输，使流式请求在收到响应头和首个响应体块后立即返回，并由迭代接口按需消费后续 ASGI `http.response.body` 消息。
