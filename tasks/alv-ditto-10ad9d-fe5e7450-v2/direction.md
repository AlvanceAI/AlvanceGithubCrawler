在 Linux/Wayland 输入后端中集成 xkb 键位映射解析，将 evdev 原始按键码转换为 compositor 配置后的逻辑按键，使 Caps Lock→Escape 等重映射能够被正确识别。
