将 Swagger UI 初始化逻辑从 index.html 的内联脚本迁移到独立的动态 JavaScript 资源端点，同时保留现有 URL、OAuth、持久化授权和展示配置，使其兼容 `script-src 'self'` CSP。
