# Scenario Workflow — 场景探索模式

系统性地发现边界、失败模式和"没人想到的情况"。

核心：种子场景 → 分解维度 → 生成情境 → 分类去重 → 展开边界 → 记录 → 循环。

## 流程

```
Phase 1: Seed — 捕获并分析种子场景
Phase 2: Decompose — 分解为探索维度
Phase 3: Generate — 生成一个新情境
Phase 4: Classify — 分类：新/变体/重复/低价值
Phase 5: Expand — 展开边界 case、what-if、失败模式
Phase 6: Log — 记录到 scenario-results.tsv
Phase 7: Repeat — 下一个未探索维度
```

## 使用方式

```bash
autoresearch
Mode: scenario
Scenario: 当用户要求 Karl Marx skill 分析零工经济时的可能失败模式
Domain: research
Iterations: 10
```

## 探索维度

| 维度 | 说明 | AKIRA 应用 |
|------|------|------------|
| **Happy path** | 正常使用流程 | skill 正确处理典型请求 |
| **Error path** | 预期失败 | skill 识别到不适用的领域并拒绝 |
| **Edge case** | 边界条件 | 请求跨多个 skill 的话题 |
| **Abuse/misuse** | 误用 | 用户试图让 skill 离开该人物的立场 |
| **Scope** | 范围溢出 | 请求超出该人物时代/领域的分析 |
| **Context** | 语境缺失 | 用户提供的背景不足以生成准确回应 |
| **Tempo** | 节奏不适配 | 用户要快速回答但该人物的风格需要展开 |
| **Contradiction** | 内部矛盾 | skill 内容和 Core/Lab 规则冲突 |
| **Integration** | 集成问题 | 和其他 skill 一起使用时的冲突 |
| **Evolution** | 演化问题 | skill 内容过时需要更新 |

## 维度优先级

1. 先走 happy path（建立基线理解）
2. Error path（最常见的真实问题）
3. Edge case（bug 藏身之处）
4. 特定维度（AKIRA → scope、context、contradiction）

## 生成策略

| 策略 | 用法 |
|------|------|
| **维度遍历** | 早期迭代，逐个维度走 |
| **组合** | 中期，组合 2 个维度（edge case + scope） |
| **否定** | 取 happy path 的一步，否定它 |
| **放大** | 取现有情境，把一个参数推到极端 |
| **角色切换** | 同场景换用户角色（专家 vs 新手） |
| **时间切换** | 同场景在不同时间（skill 刚建 vs 用了半年） |

## 分类规则

| 分类 | 标准 | 动作 |
|------|------|------|
| **New** | 没有现有情境覆盖 | KEEP |
| **Variant** | 类似但有实质差异 | KEEP（作为子场景） |
| **Duplicate** | 已被覆盖 | DISCARD |
| **Out of scope** | 不匹配种子场景 | DISCARD |
| **Low value** | 技术上可能但不现实 | DISCARD |

## 情境格式

```markdown
### [维度] 情境：描述性标题

**角色：** 谁在使用
**前置条件：** 什么必须为真
**触发：** 什么动作启动
**流程：**
1. 步骤 1
2. 步骤 2
**预期结果：** 应该发生什么
**可能失败：** 潜在故障点
**严重度：** Critical / High / Medium / Low
```

## 输出

```
scenario/{日期时间}-{slug}/
├── scenarios.md    — 按维度分组的所有情境
├── edge-cases.md   — 边界 case 和失败模式（含严重度）
├── scenario-results.tsv — 迭代日志
└── summary.md      — 摘要、覆盖矩阵、建议
```

## AKIRA Skill 的场景探索用法

对人物视角 skill，场景探索能发现：

- 该视角在哪些领域会失效？（Marx 分析量子计算？）
- 什么请求会让 skill 退化为通用回答？
- 用户提供的什么上下文会让语境重建失败？
- 什么情况下 skill 会和 Core/Lab 规则冲突？

这些发现直接喂给 Loop 模式做改进。
