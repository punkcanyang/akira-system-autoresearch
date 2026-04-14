# Autoresearch Lessons

## Lesson 1: Eval 环境必须和目标文件同源
**Date:** 2026-04-14
**Context:** 自迭代 Round 1-5 用 sandbox 模拟运行 eval，但 sandbox 无法访问 OrbStack 文件系统，导致分数失真（从 93.1 暴跌到 62.6）。
**Rule:** eval 脚本必须在能直接读写 skill 目录的环境中运行。用 `execute_code` 或 `terminal` 跑，不要在隔离 sandbox 里模拟。

## Lesson 2: 第一轮 eval 必须是真实运行
**Date:** 2026-04-14
**Context:** Round 0-5 的分数是估算/模拟的，不是真实 eval 输出。直到 Round 6 才跑了真实的 `run_eval.py`。
**Rule:** 进入循环前，Phase 2 的 baseline 必须通过实际运行 verify 命令获得，不可估算。

## Lesson 3: Substring 匹配必须对齐文件实际措辞
**Date:** 2026-04-14
**Context:** eval 脚本检查 `loop-protocol.md` 是否包含 "没有验证"，但文件用的是 "验证失败"。检查 "REVERT" 但文件用小写 "revert"。
**Rule:** 写 eval 时先 grep 确认目标文件的实际措辞，不要凭记忆写关键词。

## Lesson 4: SKILL.md 应显式引用 workflow 文件
**Date:** 2026-04-14
**Context:** SKILL.md 只写了 "详见 references/loop-protocol.md" 但没引用 reason/scenario/cascade 的文件路径，导致 architecture_coverage 扣分。
**Rule:** SKILL.md 的工作流总览应包含所有 references 文件的显式引用表。
