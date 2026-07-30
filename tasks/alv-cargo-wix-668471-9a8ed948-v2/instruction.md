Repository `volks73/cargo-wix` at commit `9a8ed9486637e1fb839f209730eda6c95fd12d88` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

改进 WiX XML/WXS 解析器，使其在提取元素及扩展信息时正确跳过 `ifdef`、`define`、`else`、`endif`、`if` 等 XML 处理指令，避免将预处理器节点误判为空标签。
