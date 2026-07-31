Repository `go-cmd/cmd` at commit `78577dc52fb738d17e9c6c49d010142a68bb186a` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

将流式标准输出和错误输出从按换行符分帧改为按固定大小字节块传递，确保无换行、超长行及 ANSI 进度输出不会导致缓冲区无限增长或 broken pipe，并由调用方自行重组数据。
