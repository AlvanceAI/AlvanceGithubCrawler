在 DCP checkpoint 的 seqNo 超过 vBucket 最新 seqNo 或服务端返回“requested value is outside range”时，将该 vBucket 的 checkpoint 自动回退到零并重新开启流，同时记录完整 checkpoint 文档内容。
