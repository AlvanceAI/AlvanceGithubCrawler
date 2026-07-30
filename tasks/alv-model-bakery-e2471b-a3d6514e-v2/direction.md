修复 Recipe 的 seq 状态管理，使 prepare_recipe 后调用 make_recipe 仍生成递增且不重复的序列值，并在测试隔离时可靠重置序列。
