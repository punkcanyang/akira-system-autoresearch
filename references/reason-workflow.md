# Reason Workflow — 对抗精炼模式

适用于主观质量评估：视角准确性、语气、craft 模拟等无法用简单数字衡量的领域。

核心机制：多 agent 盲评收敛。不是"我觉得这样更好"，而是"多个独立评审都认为这样更好"。

## 流程

```
Phase 1: Setup — 配置任务、领域、评审数量
Phase 2: Generate-A — 作者 A 生成候选版本
Phase 3: Critic — 对抗批评者攻击 A
Phase 4: Generate-B — 作者 B 看到任务+A+批评，生成 B
Phase 5: Synthesize-AB — 综合者从 A+B 中提炼 AB
Phase 6: Judge Panel — N 个盲评评审投票
Phase 7: Convergence — 检查是否收敛
Phase 8: Handoff — 输出最终结果，可选 chain
```

## 关键原则

- **冷启动隔离**：每个 agent 只看到必要信息，不共享完整上下文，防止讨好
- **随机标签**：评审看到的是 X/Y/Z，不知道哪个是 A/B/AB，防止锚定偏见
- **必须选赢家**：不允许"平局"，接近时强制排序
- **收敛判定**：当同一个候选连续赢 N 轮时停止

## 使用方式

```bash
autoresearch
Mode: reason
Task: Mark Fisher skill 是否正确捕捉了他用流行文化诊断晚期资本主义的手法？
Domain: research
Iterations: 3
Judges: 3
```

## 每个角色的职责

### Author-A（第一作者）
- 只收到任务描述
- 生成第一个候选版本
- 后续轮次收到当前获胜者，在其基础上改进

### Critic（批评者）
- 只收到候选 A（不看任务描述，防止任务锚定）
- 必须找到至少 3 个弱点
- 每个弱点标记严重度：FATAL / MAJOR / MINOR
- 只攻击，不提供修复方案

### Author-B（挑战者）
- 收到任务 + A + 批评
- 生成更好的 B，吸收批评但不被批评牵着走
- 不能只是修补 A，需要实质性不同

### Synthesizer（综合者）
- 收到任务 + A + B（不看批评和评审历史）
- 生成 AB，结合两者最强元素
- 不是折中，是选出真正好的部分再组合

### Judges（盲评评审团）
- 收到随机标签的候选（X/Y/Z）
- 评估标准：准确性、完整性、推理质量、实用性
- 必须引用具体文本来支持判断
- 不看长度，看实质

## 收敛条件

| 模式 | 停止条件 |
|------|----------|
| convergent（默认） | 同一候选连续赢 K 次（默认 3） |
| creative | 永不停止，直到用户中断 |
| bounded | 跑完 N 轮后停止 |

## 振荡检测

如果赢家交替超过 5 次没有连续赢：
- 触发振荡警告
- 停止循环
- 报告："任务可能本质上是模糊的，或者候选处于同等水平"
- 呈现所有三个候选作为等价替代

## 输出格式

### reason-lineage.jsonl

每轮追加一条记录：

```json
{
  "round": 1,
  "task_hash": "sha256",
  "label_map": {"X": "AB", "Y": "A", "Z": "B"},
  "judge_votes": [...],
  "round_winner": "AB",
  "vote_tally": {"A": 1, "B": 0, "AB": 2},
  "consecutive_wins": 1,
  "critic_weaknesses": ["FATAL: ...", "MAJOR: ..."],
  "winning_strength": "...",
  "runner_up_gap": "..."
}
```

### 最终 handoff.json

```json
{
  "task": "...",
  "domain": "research",
  "mode": "convergent",
  "rounds_run": 6,
  "converged": true,
  "final_winner": "AB",
  "converged_candidate": {"text": "...", "word_count": 312},
  "critique_themes": ["...", "..."],
  "quality_signals": {"critic_fatals_addressed": 3, "judge_consensus": 1.0}
}
```

## 与 Loop 模式的区别

| | Loop 模式 | Reason 模式 |
|---|---|---|
| 评估方式 | 机械命令验证 | 多 agent 盲评 |
| 适用领域 | 有可量化指标 | 主观质量（语气、视角、craft） |
| 决策机制 | 指标改善 = 保留 | 投票多数 = 获胜 |
| 迭代速度 | 快（秒级验证） | 慢（每次要跑多个 agent） |
| 输出 | 指标日志 TSV | lineage JSONL + handoff JSON |

## AKIRA skill 的 Reason 用法

对人物视角 skill，reason 模式特别有用：

```
Task: 检查 akira-person-ivan-illich 是否准确还原了 Illich 对制度反生产性的诊断风格
Domain: research
```

评审团会从不同角度评估 skill 的输出质量，比单一指标更可靠。
