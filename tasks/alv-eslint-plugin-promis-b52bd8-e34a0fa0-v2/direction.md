新增 ESLint 规则 `prefer-promise-static-methods`，检测执行器仅立即调用 `resolve` 或 `reject` 的 `new Promise(...)`，并自动修复为对应的 `Promise.resolve(...)` 或 `Promise.reject(...)`。
