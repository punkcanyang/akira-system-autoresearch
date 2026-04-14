# Autoresearch 实战教训

## 2026-04-14: 首次大规模实战

### 背景
- 自迭代：8 轮，81.3 → 100
- akira-system-eva：1 轮，92.3 → 100
- akira-system-core：6 轮，91.9 → 100
- akira-person-mark-fisher：2 轮（loop + reason）

### 教训 1: git repo 缺失导致 commit 失败
- **现象**：akira-system-core 没有 git repo，首次 commit 报 "Author identity unknown"
- **根因**：skill 目录从未初始化 git，且系统 git config 未设 user
- **修复**：先 `git init`，再 `git config user.email/name`（local scope）
- **预防规则**：Phase 0 必须检查 git status，不存在则初始化

### 教训 2: eval 脚本本身可能有 bug
- **现象**：`content[:200]` 范围太小，frontmatter 的 description 很长时，后面的字段（author/version）检测不到，spec_compliance 从 100 跌到 60
- **根因**：eval 用硬编码范围提取 frontmatter，没有用 `split("---")[1]`
- **修复**：改用 `content.split("---")[1]` 提取完整 frontmatter 块
- **预防规则**：第一次跑 eval 时，手动检查 eval 逻辑是否正确，特别是字符串匹配范围

### 教训 3: 模拟分数 vs 真实 eval
- **现象**：早期轮次的分数是模拟估算，真实 eval 跑出来有差异
- **根因**：没先建好 eval 脚本就凭感觉打分
- **修复**：先写 eval 脚本，再跑循环。没有 eval 就不迭代
- **预防规则**：Phase 0 必须确认 Verify 命令可执行且输出有意义

### 教训 4: 全满分时 weakest 函数报错
- **现象**：当所有维度都是 100 时，weakest 返回一个随机维度
- **根因**：`min(dimensions, key=dimensions.get)` 在全等值时行为未定义
- **修复**：全满分时 weakest 返回 "none"
- **预防规则**：eval 脚本必须处理全满分边界情况

### 教训 5: 权重总和不是 1.0
- **现象**：初版权重 sum = 0.95，天花板只有 95，永远到不了 100
- **根因**：手动分配权重时没验算
- **修复**：权重 sum 必须 = 1.0
- **预防规则**：eval 脚本添加 `assert abs(sum(weights) - 1.0) < 0.001`

### 教训 6: 系统 skills 不需要 reason 模式
- **现象**：reason 模式需要"具体场景 + 多 agent 盲评"，系统 skills 的评估维度是架构/协议/完整性，没有可盲评的"输出"
- **结论**：系统 skills 用 loop 模式即可。reason 模式留给人物视角 skills
