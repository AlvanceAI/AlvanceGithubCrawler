Repository `aws/aws-lambda-runtime-interface-emulator` at commit `a0f264ae8bd990e756f2e87c9b44610e522d801e` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 Invoke API 增加对 `X-Amz-Invocation-Type: Event` 的异步调用模拟，使请求在事件被接受后立即返回而不等待函数执行完成。
