Repository `model-bakers/model_bakery` at commit `a3d6514e60a39dadc72ebefcf951737854835300` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

修复 Recipe 的 seq 状态管理，使 prepare_recipe 后调用 make_recipe 仍生成递增且不重复的序列值，并在测试隔离时可靠重置序列。
