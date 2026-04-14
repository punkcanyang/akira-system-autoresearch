# Cascade Protocol — 级联更新机制

当一个 skill 被修改后，哪些相关 skill 需要同步检查。

## 原则

级联是**标记需要 review**，不是自动修改。原因：技能之间的依赖关系复杂，盲目自动改可能引入不一致。

## 依赖关系图

```
System-Core（底盘）
  ├── 所有 skill 都依赖 Core 的坐标系和回收框架
  └── Core 改动 → 全量检查

System-Drug-Skill-Lab（药物工厂）
  ├── 所有药物 skill 依赖 Lab 的 intake 流程
  └── Lab 改动 → 所有 akira-drug-* skill

System-EVA（视角蒸馏）
  ├── 所有人物 skill 依赖 EVA 的生成流程
  └── EVA 改动 → 所有 akira-person-* skill

System-Skill-Design（架构设计）
  └── Design 改动 → 所有 skill（架构模板变更）

单药物 skill
  └── 药物改动 → Core（如果回收框架涉及该药物）

单人物 skill
  └── 人物改动 → Core（如果引用了该人物的某些观点）

单人物 skill → 同体系人物
  └── 如 akira-person-karl-marx 改动 → akira-person-karl-nietzsche（可能有引用）
```

## 级联触发规则

| 触发条件 | 级联目标 | 优先级 |
|----------|----------|--------|
| 修改了 System-Core 的坐标系定义 | 所有 skill | Critical |
| 修改了 System-Core 的回收框架 | 所有药物 skill | Critical |
| 修改了 Drug-Skill-Lab 的 intake 流程 | 所有药物 skill | High |
| 修改了 EVA 的生成流程 | 所有人物 skill | High |
| 修改了 Skill-Design 的架构模板 | 所有 skill | High |
| 修改了药物 skill 的回收框架部分 | Core（引用检查） | Medium |
| 修改了人物 skill 的核心观点 | Core（引用检查） | Medium |
| 修改了人物 skill 的 craft 部分 | EVA（流程检查） | Low |
| 修改了药物 skill 的证据来源 | Drug-Skill-Lab（数据流检查） | Low |

## 级联流程

```
1. 确定修改了什么（git diff 分析）
2. 查询依赖关系图，找到级联目标
3. 对每个级联目标：
   a. 检查是否引用了被修改的内容
   b. 如果引用了：标记为 NEEDS_REVIEW
   c. 如果没引用：标记为 CHECK_RECOMMENDED
4. 生成级联报告
5. 用户决定是否执行 review
```

## 级联报告格式

```markdown
## 级联报告 — {修改的 skill}

**修改类型：** {Core 坐标系 / 回收框架 / 药物数据 / 人物视角 / ...}

| Skill | 状态 | 原因 |
|-------|------|------|
| akira-system-core | NEEDS_REVIEW | 回收框架引用了该药物 |
| akira-lsd | CHECK_RECOMMENDED | 可能受坐标系变更影响 |
| akira-person-mark-fisher | OK | 无直接依赖 |
```

## 自动 vs 手动

- `Cascade: auto` — 生成报告后自动对 NEEDS_REVIEW 的 skill 跑 eval
- `Cascade: manual`（默认）— 只生成报告，等用户指示
- `Cascade: off` — 不检查级联
