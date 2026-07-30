为 pagerduty_service_dependency 资源增加计划阶段的环依赖检测，使直接或间接形成服务依赖环的配置在 terraform plan 时即报错，而非 apply 时由 PagerDuty API 拒绝。
