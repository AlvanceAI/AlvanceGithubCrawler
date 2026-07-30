为 vultr_instance 资源新增支持 Terraform ephemeral 值的只写 user_data_wo 属性及版本触发机制，确保敏感初始化数据可发送至 Vultr API但不持久化到 state。
