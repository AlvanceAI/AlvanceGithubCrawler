Repository `voxpupuli/puppetboard` at commit `434b9cf9e3e7477b09a88886d073c520dc610155` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

重构 Puppetboard 的 WSGI 初始化流程，消除导入时的 PuppetDB 连接、版本检查、进程退出和日志配置副作用，并提供可选检查、日志及字典配置的 bootstrap() 入口。
