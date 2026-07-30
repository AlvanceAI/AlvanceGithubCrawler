Repository `PagerDuty/terraform-provider-pagerduty` at commit `86fd7379934b24d3964b161bbda463aa691e78a0` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 pagerduty_service_dependency 资源增加计划阶段的环依赖检测，使直接或间接形成服务依赖环的配置在 terraform plan 时即报错，而非 apply 时由 PagerDuty API 拒绝。
