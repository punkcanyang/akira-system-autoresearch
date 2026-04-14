# Reason 模式评估：akira-person-dan-koe

**日期**: 2026-04-14  
**模式**: reason (convergent, 3 judges)  
**领域**: research  
**评估者**: Hermes Agent (akira-system-autoresearch reason workflow)

---

## 任务

评估 akira-person-dan-koe skill 的整体质量：视角准确性、语境重建、工艺模拟、声音区分度、未来推演、引用完整性，以及通用维度（架构完整度、文档质量、规范遵从度、可复现性）。

---

## Phase 2-5: 候选版本与对抗批评

### Generate-A（初版评估）

Skill 整体结构完整，5 个 core lenses（identity precedes behavior, one-person business as leverage, clarity makes discipline natural, life is a system, writing is thinking）覆盖了 Dan Koe 的核心主张。表达质地（expression texture）、决策启发式（decision heuristics）、价值排序（value ordering）等模块设计合理，体现了 AKIRA person skill 的标准结构。

### Critic（对抗批评）

**FATAL: 引用材料严重不足**  
extraction-framework.md 仅 20 行，内容泛化，未体现 Dan Koe 具体的方法论步骤。tension-checklist.md 仅 7 行 2 条张力。evidence-map.yaml 仅 4 条 claim，其中多条依赖二手来源（Binance 转述）。SKILL.md 末尾引用 `data/profile.yaml`，但该文件不存在。整体引用密度远低于同系列其他 person skill（如 illich、fisher）。

**MAJOR: 语境重建场景空洞**  
"Context reconstruction" 定义了 4 种语境（书写、访谈、演讲、被追问），但每种描述都是抽象特征描述（"概念密度高""偏观点输出型"），没有附带任何实际语料样本。对比其他 skill 的做法（附带原始摘录或模拟段落），这里的语境重建更像是标签分类而非场景还原。

**MAJOR: 缺少实际内容产出示例**  
整个 skill 没有一段 Dan Koe 的原始文字摘录、newsletter 片段或视频 transcript。"語料庫" 部分的引用是模拟生成的，而非来自实际来源。这意味着 skill 的 craft 模拟缺乏验证基线——我们不知道模拟得像不像，因为没有原始材料可对比。

**MINOR: 未来推演缺乏深度**  
Foresight 部分仅 2-3 句话，没有对具体场景的推演示例。对比 skill 对自己的要求（"涉及趋势、未来时，不只谈焦虑"），这里恰恰只谈了方向没有展开。

**MINOR: 安装文档引用不存在的目录**  
README.md 提到 `templates/` 和 `scripts/` 子目录，但实际不存在。README 中的 "References to load when needed" 引用了 `data/profile.yaml`，同样不存在。

### Generate-B（改进版评估视角）

B 版本在 A 的基础上更严格地审视了「可复现性」维度。一个 skill 的质量不只是它写了什么，而是另一个 agent 能否仅凭这些文件复现同等质量的输出。Dan Koe skill 在这个问题上表现不一致：核心框架（lenses, heuristics, expression texture）足够清晰，但支撑材料（references, data）薄弱，导致复现高度依赖 agent 自身的推断能力而非 skill 提供的证据。

### Synthesize-AB（综合评估）

Skill 的骨架（SKILL.md 主体结构、5 个 core lenses、answer protocol、decision heuristics）是扎实的，体现了 AKIRA person skill 设计的高水准。但肌肉（references、data、语料样本）严重不足。这是一个「结构完整但内容饥饿」的 skill。

---

## Phase 6: 盲评评审团

### 评审 1（架构视角）

关注 skill 的文件完整度和结构设计。SKILL.md frontmatter 规范，模块齐全（scope, identity snapshot, core lenses, domain craft, decision heuristics, value ordering, expression texture, context reconstruction, tensions, foresight, answer protocol, sources）。**架构维度给分 100**。但引用文件严重不足拖累了整体评分。

### 评审 2（内容视角）

关注视角还原度和语料支撑。5 个 core lenses 准确抓住了 Dan Koe 的核心主张，特别是 identity precedes behavior 和 writing as leverage 这两个命题有明确的来源标注。**视角准确性给分 75**。但没有任何一手语料，voice distinction 的验证缺乏基线。

### 评审 3（实用视角）

关注其他 agent 能否直接使用这个 skill。SKILL.md 的 answer protocol 清晰可执行，references 指向机制合理。但 `data/profile.yaml` 不存在会导致按需加载失败，且 references 内容太薄，agent 在复杂问题上会缺乏足够的「弹药」。**可复现性给分 60**。

---

## Phase 7: 评估分数

### 各维度评分

| 维度 | 类别 | 权重 | 评分 (0-100) | 说明 |
|------|------|------|-------------|------|
| 架构完整度 | 通用 | 15% | **100** | frontmatter、README、refs/data/evals 目录齐全，结构完全符合标准 |
| 文档质量 | 通用 | 10% | **85** | README 清晰、安装说明完整、跨 agent 适配有指导 |
| 规范遵从度 | 通用 | 10% | **85** | 符合 hermes-skill-authoring-standard，frontmatter 规范 |
| 可复现性 | 通用 | 5% | **60** | 核心框架可复现，但引用的 data/profile.yaml 不存在，refs 材料不足 |
| 视角准确性 | Person | 20% | **75** | 5 个 lenses 准确抓住核心主张，但来源以二手为主 |
| 语境重建 | Person | 15% | **60** | 4 种语境有定义但缺实际样本，更像标签分类而非场景还原 |
| 工艺模拟 | Person | 15% | **70** | Domain craft 描述合理，extraction-framework 太简略 |
| 声音区分度 | Person | 5% | **75** | Expression texture 模块有效区分，但缺原始语料对比 |
| 未来推演 | Person | 5% | **55** | 仅方向性判断，无具体推演场景 |
| 引用完整性 | Person | 5% | **45** | 核心引用文件薄弱，无一手语料，profile.yaml 缺失 |

### 加权总分

```
总分 = (100×0.15) + (85×0.10) + (85×0.10) + (60×0.05)
     + (75×0.20) + (60×0.15) + (70×0.15) + (75×0.05) + (55×0.05) + (45×0.05)

     = 15.0 + 8.5 + 8.5 + 3.0
     + 15.0 + 9.0 + 10.5 + 3.75 + 2.75 + 2.25

     = 78.25 / 100
```

**综合评分：78.25 / 100**

---

## Phase 8: 总结

### 最强维度

| 排名 | 维度 | 分数 | 说明 |
|------|------|------|------|
| 🥇 | **架构完整度** | 100 | 文件结构完全符合 AKIRA person skill 标准，模块齐全 |
| 🥈 | **文档质量** | 85 | README 清晰，跨 agent 适配有实质指导 |
| 🥈 | **规范遵从度** | 85 | frontmatter、answer protocol、references 机制均规范 |

### 最弱维度

| 排名 | 维度 | 分数 | 说明 |
|------|------|------|------|
| ⚠️ | **引用完整性** | 45 | 无一手语料，核心引用文件（profile.yaml）缺失，evidence-map 仅 4 条 |
| ⚠️ | **未来推演** | 55 | 只有方向性判断，没有具体推演场景和推理过程 |
| ⚠️ | **语境重建** | 60 | 语境描述抽象，没有实际语料样本支撑场景还原 |

### 改进建议

#### 🔴 P0 — 必须修复

1. **补全缺失文件**
   - 创建 `data/profile.yaml`（README 已引用但不存在）
   - 创建 `templates/` 和 `scripts/` 目录或从 README 中移除引用
   - 创建 `data/` 目录下的 `texts.yaml` 存储关键语料片段

2. **充实 evidence-map.yaml**
   - 当前仅 4 条 claim，至少补充到 10+ 条
   - 每条 claim 标注具体来源（URL、视频时间戳、文章标题）
   - 将 evidence_level 提升：减少 B 级来源，增加 A 级（官方站点、Substack 原文）

#### 🟡 P1 — 强烈建议

3. **补充一手语料**
   - 从 Substack newsletter 提取 3-5 段代表性原文
   - 从 YouTube 视频提取 2-3 段 transcript
   - 将语料存入 `data/texts.yaml`，在 SKILL.md 的「語料庫」部分引用实际来源而非模拟

4. **扩展 extraction-framework.md**
   - 当前仅 20 行，补充 Dan Koe 的具体「压缩」方法论步骤
   - 描述他如何从一个抽象问题 → 重新命名 → 认知框架 → 可操作步骤的具体过程
   - 对比其他 person skill 的 extraction-framework（如 illich 的制度分析方法）

5. **深化未来推演模块**
   - Foresight 部分增加 2-3 个具体推演场景
   - 例如：「如果 AI 能在 5 分钟内写出 Dan Koe 风格的文章，他的 one-person business 模型如何应对？」
   - 使用 answer protocol 中的推演方法，而非仅列方向

#### 🟢 P2 — 可选优化

6. **扩展 tension-checklist.md**
   - 当前仅 2 条张力，补充至少 3-4 条
   - 例如：「系统化思维 vs 过度抽象的人生理解」「高确定度表达 vs 缺乏实证支撑」

7. **增加语境重建的实际样本**
   - 在 Context reconstruction 每种语境下附带一段模拟输出或原始摘录
   - 让其他 agent 能直接对比「这个语境下应该是什么样的」

8. **建立与其他 person skill 的对话**
   - SKILL.md 中已提到与 Naval Ravikant、Pieter Levels 的结构性对应
   - 可以扩展为 cross-reference 模块，标注 Dan Koe 视角与其他视角的交汇与分歧

---

## Convergence

评估结果在 3 轮评审中收敛：**引用材料不足**是贯穿所有评审的一致批评。架构和文档质量稳定高分，内容深度稳定偏低。结论明确：这是一个「骨架优秀、肌肉待补」的 skill。

**converged: true**  
**final_winner: AB (综合评估)**  
**reason_score: 78.25**
