实现 6502 CPU 的 CLI、SEI、PLP 中断屏蔽标志延迟生效，以及 BRK/IRQ 被同时到达的 NMI 劫持并改用 $FFFA 向量的精确时序行为。
