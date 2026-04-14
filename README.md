# AKIRA System Autoresearch

域无关的自主迭代研究引擎。融合 Karpathy autoresearch 核心循环与 uditgoenka 的泛化工作流。

## 核心原理

源自 Karpathy 的 autoresearch 项目：

> 约束即自由。一个指标、一个范围、原子修改、机械验证、git 记忆。循环，直到变好。

- 原始项目：https://github.com/karpathy/autoresearch
- 泛化版本：https://github.com/uditgoenka/autoresearch
- Codex 移植：https://github.com/codex-autoresearch

## 三种模式

| 模式 | 用途 | 适合场景 |
|------|------|----------|
| **loop** | 优化迭代 | 有可量化指标的改进任务 |
| **reason** | 对抗精炼 | 主观质量评估（视角、语气、craft） |
| **scenario** | 场景探索 | 发现边界、失败模式、盲区 |

## 安装

### 作为 Hermes Skill

```bash
# 克隆或复制到 skills 目录
cp -r akira-system-autoresearch ~/.hermes/skills/autonomous-ai-agents/
```

### 跨 Agent 适配

本 skill 设计为 Hermes Agent 专用，但核心协议域无关：

- **Claude Code**：参考 uditgoenka/autoresearch 的 Claude plugin 结构
- **Codex**：参考 codex-autoresearch 的 hook 机制
- **其他 agent**：核心循环（Phase 0-9）可直接移植，工作流模式需要适配 agent 的多 agent 能力

关键适配点：
1. `Verify` 命令的执行方式（terminal tool / subprocess / shell）
2. `git` 操作的权限范围
3. 多 agent 隔离（reason 模式需要）
4. 结果日志的持久化位置

## 文件结构

```
akira-system-autoresearch/
├── SKILL.md              — 主入口，定义触发条件和使用方式
├── README.md             — 本文件
├── references/
│   ├── loop-protocol.md  — 核心循环详细协议（Phase 0-9）
│   ├── eval-dimensions.md — AKIRA skill 评估维度
│   ├── reason-workflow.md — 对抗精炼工作流
│   ├── scenario-workflow.md — 场景探索工作流
│   └── cascade-protocol.md — 级联更新机制
├── data/                 — 评估数据（待建）
├── evals/                — 评估脚本（待建）
└── scripts/              — 辅助脚本（待建）
```

## 与其他 AKIRA System 的关系

- **System-Core**：定义了基线坐标系和回收框架，autoresearch 的药物 skill 迭代必须遵循
- **System-Drug-Skill-Lab**：药物资料的 intake 流程变更会触发级联
- **System-EVA**：人物视角的生成流程变更会触发级联
- **System-Skill-Design**：架构模板变更会触发级联

## 设计决策

### 为什么合并 Karpathy 和 uditgoenka？

Karpathy 的版本纯粹、简洁，核心循环打磨得很好（卡住恢复、协议重锚、教训提取）。
uditgoenka 的版本泛化了领域，增加了 reason（对抗精炼）和 scenario（场景探索）两种模式。

两者不矛盾，是同一个核心理念在不同抽象层的实现：
- Karpathy = 优化循环的极致打磨
- uditgoenka = 工作流编排的泛化

本 skill 取两者之长：用 Karpathy 的循环质量 + uditgoenka 的工作流多样性。

### 为什么不用简单的 eval 脚本？

AKIRA 的核心问题是主观质量评估（"这个 skill 有没有抓住 Illich 的语气"）。
简单 eval 脚本能测架构完整度，但测不了视角准确性。
reason 模式通过多 agent 盲评来解决这个问题。

## 作者

AKIRA & Punkcan
- https://punkcan.art/
- https://x.com/punkcan
