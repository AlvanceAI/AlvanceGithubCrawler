为 StreamInterface 增加可表示空传输及多字节有效性的 data mask，并让 USBStreamOutEndpoint 正确标记 ZLP/满包传输边界，同时提供忽略空数据拍的简单与缓冲过滤器。
