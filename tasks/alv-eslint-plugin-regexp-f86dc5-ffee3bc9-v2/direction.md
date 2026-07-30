扩展正则表达式静态值分析，跟踪数组经 push、unshift 等原地方法添加的元素，避免 no-empty-group 与 no-empty-capturing-group 将动态填充后 join 的内容误判为空。
