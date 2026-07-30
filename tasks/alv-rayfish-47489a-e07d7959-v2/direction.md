实现可持久化的 IPv6-only 运行模式：不配置 Rayfish IPv4 TUN/CGNAT 路由，过滤 Tailscale IPv6 候选地址，提供 IPv6 Magic DNS，并在缺少 split-DNS 后端时拒绝改写全局 resolv.conf。
