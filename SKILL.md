---
name: akira-system-autoresearch
version: 0.1.0
last_updated: "2026-04-14"
author: "AKIRA & Punkcan"
description: "域无关的自主迭代研究引擎。融合 Karpathy autoresearch 核心循环（原子实验 + 机械验证 + git 记忆 + 卡住恢复）与 uditgoenka 的泛化工作流（对抗精炼 + 场景探索）。专为 AKIRA 系列 skills 的持续进化设计，同时支持任意研究领域。"
dependencies:
  - git
  - hermes-agent
---

# AKIRA System Autoresearch

> 约束即自由。一个指标、一个范围、原子修改、机械验证、git 记忆。循环，直到变好。

## What This Is

域无关的自主迭代引擎。核心循环来自 Karpathy 的 autoresearch 原理：

**修改 → 验证 → 保留/丢弃 → 循环**

在此基础上扩展了两种工作流模式：

| 模式 | 用途 | 来源 |
|------|------|------|
| **loop** | 优化迭代：改一个东西，测一个指标 | Karpathy 核心循环 |
| **reason** | 对抗精炼：多 agent 盲评收敛 | uditgoenka reason |
| **scenario** | 场景探索：系统性发现边界和失败模式 | uditgoenka scenario |

## 触发条件

用户说 "研究 X"、"迭代 Y"、"优化 Z"、"autoresearch" 时加载此 skill。

## 使用方式

```
autoresearch
Goal: 提升 akira-person-mark-fisher 的视角准确性
Scope: ~/.hermes/skills/autonomous-ai-agents/akira-person-mark-fisher/
Metric: eval_score (higher is better)
Verify: ./eval.sh
Mode: loop
Iterations: 10
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `Goal` | ✅ | 目标，用自然语言描述 |
| `Scope` | ✅ | 允许修改的文件范围（glob 或路径） |
| `Metric` | ✅ | 要优化的指标名（越高越好或越低越好） |
| `Verify` | ✅ | 输出指标值的 shell 命令 |
| `Mode` | ❌ | `loop` / `reason` / `scenario`，默认 `loop` |
| `Guard` | ❌ | 安全守卫命令，通过才能保留 |
| `Iterations` | ❌ | 迭代次数，默认无上限 |
| `Cascade` | ❌ | 是否级联更新相关 skill，默认 `auto` |

## 快速上手

### 1. 改进单个 AKIRA skill

```bash
# 进入 skill 目录，看 eval 怎么跑
cd ~/.hermes/skills/autonomous-ai-agents/akira-person-mark-fisher/
cat evals/*.py  # 理解评估维度

# 在 Hermes 中触发
autoresearch
Goal: 让 Mark Fisher skill 更准确地捕捉资本主义现实主义的诊断语气
Scope: ~/.hermes/skills/autonomous-ai-agents/akira-person-mark-fisher/
Metric: eval_total_score (higher is better)
Verify: python3 evals/run_eval.py 2>&1 | grep 'total_score' | awk '{print $2}'
Iterations: 5
```

### 2. 用 reason 模式精炼主观质量

```bash
autoresearch
Mode: reason
Task: Ivan Illich skill 是否正确体现了他对制度反生产性的诊断风格？
Domain: research
Iterations: 3
```

### 3. 用 scenario 模式探索 skill 的边界

```bash
autoresearch
Mode: scenario
Scenario: 当用户要求 Karl Marx skill 分析当代零工经济时，它会怎么失败？
Domain: research
Iterations: 10
```

## 8 条核心法则

1. **约束即自由** — 范围小到能完全理解，才能自主迭代
2. **人定方向，Agent 执行** — 用户说 WHY，agent 处理 HOW
3. **指标必须机械** — 如果不能用命令验证好坏，循环还没准备好
4. **验证要快** — 慢验证杀死迭代速度
5. **每次只改一个东西** — 原子实验建立因果链
6. **Git 是记忆** — 每次实验都提交，失败的回滚，成功的留下
7. **简单性是决胜因素** — 指标相同 + 更简单 = 赢
8. **诚实面对限制** — 做不到就说，猜不如停

## 工作流程总览

```
Phase 0: 前置检查 — git 状态、scope 存在、baseline 建立
Phase 1: 回顾 — 读文件、读结果日志、读 git 历史
Phase 2: 基线 — 跑 verify 命令，记录初始指标
Phase 3: 构思 — 选择一个假设，用四视角过滤
Phase 4: 修改 — 一个原子改动
Phase 5: 提交 — experiment: 描述
Phase 6: 验证 — 跑 verify 命令
Phase 6.5: 守卫 — 跑 guard 命令（如果有）
Phase 7: 决策 — 保留还是丢弃？
Phase 8: 记录 — 写入结果日志
Phase 8.5: 健康检查
Phase 9: 循环 → 回到 Phase 1
```

详细协议见 `references/loop-protocol.md`。

### 卡住恢复

连续 discard → REVERT / PIVOT / REFINE，详见 `references/loop-protocol.md`。

### Context Drift 防护

长迭代中定期重锚，详见 `references/loop-protocol.md`。

## 工作流扩展

| 文件 | 用途 |
|------|------|
| `references/reason-workflow.md` | 对抗精炼：多 agent 盲评收敛 |
| `references/scenario-workflow.md` | 场景探索：系统性发现边界和失败模式 |
| `references/cascade-protocol.md` | 级联更新：改一个 skill → 检查相关 skill 是否需要同步 |

## 协同关系

本 skill 与以下 AKIRA 系统 skill 协同：

- **akira-system-core** — 提供基线架构、坐标轴、维度进入/现实回收框架。当 Core 更新时，本 skill 的 eval 维度需要同步调整。
- **akira-system-eva** — EVA 负责生成人物/视角 skills。迭代 person skill 时，本 skill 的 loop 模式负责优化，EVA 负责骨架重建。
- **akira-system-drug-skill-lab** — Drug-Skill-Lab 负责药物资料的 intake 和分流。迭代 drug skill 时，本 skill 提供持续改进机制，Drug-Skill-Lab 定义证据等级和字段映射。
- **akira-system-skill-design** — 定义多药物/多状态人格偏移系统的分层架构。本 skill 的级联机制依赖 Skill Design 的架构模板来判断哪些 skill 需要同步。

## 评估维度（AKIRA 专用）

AKIRA skills 按类型有不同的评估标准。详见 `references/eval-dimensions.md`。

**通用维度：**
- 架构完整度 — 目录结构、frontmatter、refs/data/evals
- 文档质量 — README、安装说明、跨 agent 适配
- 规范遵从度 — hermes-skill-authoring-standard

**人物视角 skill 额外维度：**
- 视角准确性 — 是否抓住了该人的核心关注
- 语境重建 — 是否还原了写作/访谈/演讲/被追问的场景
- 工艺模拟 — 是否体现了专业 craft（不只是观点复述）
- 声音区分度 — 和其他视角是否明显不同
- 未来推演 — 是否能用该视角推断未发生的事

**药物 skill 额外维度：**
- 机制精准度 — 药理描述是否准确
- 坐标轴对齐 — 是否遵循 Core 的共享坐标系
- 回收框架完整度 — 维度进入、现实回收、后遗残留 5 面向
- 证据等级 — 信息来源是否标注清楚

## 级联机制

当一个 skill 被修改后，系统检查哪些相关 skill 需要同步更新：

| 修改类型 | 触发级联 |
|----------|----------|
| 人物视角 skill | Core（如果引用了该人物） |
| 药物 skill | Core（如果回收框架涉及该药物）、Drug-Skill-Lab（流程变更） |
| Core 系统 | 所有 skill — 全局检查 |
| EVA 系统 | 所有 person skill — 生成流程变更 |
| Skill Design 系统 | 所有 skill — 架构模板变更 |

级联检查是标记需要 review，不是自动修改。

## 元改进

工具自身也在迭代范围内：

```
autoresearch
Goal: 让 autoresearch 的 eval 维度更准确地预测 skill 质量
Scope: ~/.hermes/skills/autonomous-ai-agents/akira-system-autoresearch/
Metric: eval_correlation (higher is better — eval 分数与人工评审的一致性)
Verify: python3 meta_eval.py 2>&1 | grep 'correlation' | awk '{print $2}'
```

## 安全层

- 所有改动走 git 分支 + diff，不直接改主分支
- 用户 review 后才合并
- 破坏性操作（删除文件、大规模重写）必须在 Phase 0 预先批准
- 回滚用 `git revert`（保留历史），不用 `git reset --hard`（除非隔离分支）
