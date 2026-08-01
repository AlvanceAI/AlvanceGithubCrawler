移除 LexerSnapshot 抽象，使解析器直接基于 lexer state 读取 token，并同步更新相关解析流程、类型定义与测试。
