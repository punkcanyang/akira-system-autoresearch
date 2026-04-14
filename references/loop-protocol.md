# Core Loop Protocol

详细的迭代循环协议。基于 Karpathy autoresearch 原理，泛化到任意领域。

## 循环模式

- **unbounded（默认）**：一直跑直到中断
- **bounded**：指定 `Iterations: N` 跑 N 次后停止

## 必需输入

进入循环前确认：

- `Goal` — 要达成什么
- `Scope` — 允许修改哪些文件
- `Metric` — 指标名称和方向（higher/lower）
- `Verify` — 输出指标值的命令

可选：

- `Guard` — 安全守卫命令
- `Iterations` — 迭代上限
- `Cascade` — 级联模式（auto/manual/off）

---

## Phase 0: 前置检查

在进入循环前必须全部通过（全 pass 才能进入循环，任一 fail 立即停止）：

```
1. git 仓库存在？→ git rev-parse --git-dir          [判定: exit code 0 = pass]
2. 工作区干净？→ git status --porcelain               [判定: 空输出 = pass]
3. Scope 路径存在？                                     [判定: ls 能列出 = pass]
4. Verify 命令可执行？                                  [判定: 能运行并输出数值 = pass]
5. Guard 命令可执行？（如果配置了）                     [判定: 能运行并输出 pass/fail = pass]
6. 相关文件已读取？（当前状态）                         [判定: 文件内容在上下文中 = pass]
```

如果任何检查失败：停止，报错，等用户修复。

**安全检查：**
- 确认不在主分支上跑破坏性实验（建议用专用实验分支）
- 如果 Guard 配置了但不是 pass/fail 类型，确认能解析为数值
- 确认用户批准了回滚策略

---

## Phase 1: 回顾

每次迭代开始时，建立态势感知：

```
1. 读取 scope 内所有文件的当前状态
2. 读取最近 10-20 条结果日志
3. git log --oneline -20 — 看最近实验序列
4. git diff HEAD~1 — 看上次保留的改动（如果有的话）
5. 识别：什么有效、什么失败、什么没试过
6. 读取 autoresearch-lessons.md（如果存在）
```

**为什么每次都要读 git 历史？** 回滚后状态可能不是你预期的样子。git log 显示哪些实验被保留、哪些被回滚。

---

## Phase 2: 基线

在做任何修改之前，先跑一遍 Verify：

```
BASELINE=$(<verify command>)
记录：baseline 值、当前 commit hash、简短描述
```

如果基线本身就跑不通：不要进入循环，先修复设置或切换到 debug 模式。

---

## Phase 3: 构思

选择一个具体的假设。**每次只选一个。**

### 四视角过滤

在确定假设前，从四个角度审视：

| 视角 | 问题 |
|------|------|
| **乐观者** | 最有影响力的改动是什么？ |
| **怀疑者** | 这为什么会失败？（对照结果日志） |
| **历史学家** | 过去的结果和教训怎么说？ |
| **极简主义者** | 有没有更简单的版本？ |

对显而易见的机械修复可以跳过四视角。

### 假设优先级

1. 修复上次迭代的崩溃/失败
2. 利用成功方向 — 试变体
3. 探索新思路 — 受教训和视角启发
4. 保持指标不变的情况下简化
5. 小改动卡住时，尝试更大胆的改变

**好的假设：**
- "把 dropout 从 0.3 改成 0.5 看看 val_bpb 有没有降"
- "给 auth 边界情况加测试提升覆盖率"
- "内联热路径减少分配"

**坏的假设：**
- "重构几个模块看看效果"
- "清理一下"

---

## Phase 4: 修改

做**一个**聚焦的改动。

规则：
- 改动能用一句话说清
- 不要扩大 scope
- 如果需要改 scope 外的文件，放弃这个假设，记录限制，换一个在 scope 内的方案

---

## Phase 5: 提交

在验证前提交（启用干净回滚）：

```bash
git add -- <scope 文件>
git diff --cached --name-only  # 确认只提交了预期文件
git commit -m "experiment(<scope>): <改了什么和为什么>"
```

规则：
- 只提交实验相关的文件
- 不提交 autoresearch 自己的产物文件（results.tsv 等）
- 如果没有 diff，记录 `no-op` 跳过
- 用 `experiment:` 前缀

---

## Phase 6: 验证

跑 Verify 命令，捕获：
- 指标值
- stdout/stderr 摘要
- 耗时
- 是否崩溃

**超时规则：** 如果验证耗时 > 基线耗时的 2 倍，视为失败迭代。

### 验证失败处理

| 情况 | 处理 |
|------|------|
| 命令返回非零 exit code | 检查是否本次改动导致。如果是 → 回滚（discard）。如果 verify 命令本身坏了 → 硬阻断，修复 verify |
| 命令返回零但输出为空 | 3 次重试（可能的 flaky）。仍无输出 → 回滚（discard），记录 `empty_verify` |
| 输出无法解析为数值 | 回滚，记录 `unparseable_verify`。检查 verify 命令是否兼容当前 scope |
| 超时（> 2× baseline） | 回滚（discard），记录 `timeout`。改动可能引入了性能退化 |

**关键原则：** 验证失败时永远不能进入 keep 判决。宁可 discard 一个可能好的改动，也不能带着不确定的指标继续。

---

## Phase 6.5: 守卫

如果配置了 Guard，在指标改善后运行：

- Verify 回答 "指标有没有改善？"
- Guard 回答 "改动有没有破坏别的东西？"

Guard 失败 → 回滚 → 记录为 discard（因为 guard 失败）

---

## Phase 7: 决策

### 保留（keep）

满足以下全部：
- 指标按预期方向改善
- Guard 通过（或没有 Guard）
- 复杂度代价合理

### 丢弃（discard）

满足任一：
- 指标持平或退步
- Guard 失败
- 改动带来的复杂度不值得微小收益

#### 简单性覆盖

- 微小改善（< 1%）+ 显著复杂度增加 → 丢弃
- 指标不变 + 代码更简单 → 保留

### 回滚

```bash
# 首选：git revert（保留历史）
git revert HEAD --no-edit

# 备选：git reset（如果 revert 有冲突）
git revert --abort && git reset --hard HEAD~1
```

优先用 `git revert`，保留实验记录供后续学习。

### 崩溃处理

1. 检查错误
2. 如果假设仍然有效，修复 trivial 错误重试（最多 3 次）
3. 否则回滚，记录 `crash`

---

## Phase 8: 记录

追加到结果日志（TSV 格式）：

```
iteration  commit   metric  delta   guard  status    description
0          a1b2c3d  85.2    0.0     pass   baseline  初始状态
1          b2c3d4e  87.1    +1.9    pass   keep      添加 auth 边界测试
2          -        86.5    -0.6    -      discard   重构 test helpers（破坏了 2 个测试）
```

---

## Phase 8.5: Health Check（健康检查）

每 10 次迭代或检测到异常时：

```
1. 磁盘空间 → df -h（剩余 < 1GB 触发警告）
2. git 状态完整性 → git fsck（无 dangling objects = healthy）
3. Verify 命令是否仍然可用（跑一次确认能输出数值）
4. 结果日志一致性 → 行数 = 迭代次数 + 1（含 header）
```

**Health 判定规则：**
- 全部 healthy → 继续
- 任一 unhealthy → 降级为 warning，记录但不阻断
- git 损坏 → 硬阻断，停止循环
- 磁盘 < 500MB → 硬阻断，停止循环

---

## Phase 9: 循环

### Bounded 模式
- 跑完 N 次后停止
- 打印摘要

### Unbounded 模式
- 继续直到：目标达成 / 用户中断 / 硬阻断器出现
- 不要问 "要不要继续？"

### 卡住恢复（PIVOT/REFINE）

| 信号 | 动作 |
|------|------|
| 连续 3 次 discard | **REFINE**：在当前策略内调整，换参数/目标文件 |
| 连续 5 次 discard | **PIVOT**：彻底放弃当前策略，重新读取所有文件，选完全不同方向 |
| 2 次 PIVOT 无改善 | 尝试搜索外部信息（如果可用） |
| 3 次 PIVOT 无改善 | 软阻断：停止当前 run，报告需要人工审查或更广 scope |

任何一次 `keep` 重置所有计数器。

每次 PIVOT 后提取一条 lesson 写入 `autoresearch-lessons.md`。

---

## 进度报告

每 5 次迭代和完成时，总结：
- 基线 vs 最佳指标
- keep/discard/crash 计数
- 最近几次状态
- 下一步可能方向

## Context Drift 防护

长迭代中，agent 可能逐渐偏离原始协议（偏离 scope、忘记约束、混淆维度）。需要定期重锚。

### 触发条件

| 信号 | 动作 |
|------|------|
| 每 5 次迭代 | 轻量重锚：重新读取 SKILL.md 核心法则，确认目标和 scope 不变 |
| 检测到 scope 跨越 | 立即停止：如果发现改动了 scope 外的文件，回滚到上次安全状态，重读 scope 定义 |
| 指标方向反转 | 审查：是否在优化错误的指标？重新确认 Metric 定义 |
| 连续 2 次 PIVOT | 强制重锚：重新读取所有文件（SKILL.md + references + 历史结果），检查是否有被忽略的约束 |

### 重锚协议

```
1. 暂停当前迭代
2. 重新读取 SKILL.md 中的 "必需输入" 部分
3. 确认：Goal 仍然是 __？Scope 仍然是 __？Metric 仍然是 __？
4. git diff --stat HEAD~5 — 最近 5 次改动的范围是否合理？
5. 如果发现漂移：回滚漂移部分，记录 lesson
6. 恢复迭代
```

**关键原则：** 重锚不丢人。自动重锚是健康系统的表现，不是故障。

---

## 硬阻断器（立即停止）

- Verify 命令不可用或输出无法解析
- Scope 文件被外部删除
- git 仓库损坏
- 磁盘耗尽
- 同一崩溃连续 5 次无变化
- 用户中断
- 需要未批准的外部操作
