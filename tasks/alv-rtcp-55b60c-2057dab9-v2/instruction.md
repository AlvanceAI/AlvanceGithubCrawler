Repository `pion/rtcp` at commit `2057dab9914c82c5dec0625bc801c41244b8d353` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为各类 RTCP 包的长度不足解析失败提供可区分、可通过 errors.Is/errors.As 筛选的错误，使调用方能够单独忽略 SDES 等非关键畸形包错误。
