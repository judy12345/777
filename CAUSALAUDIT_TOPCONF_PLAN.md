# CausalAudit 顶会导向研究蓝图（CCS / S&P / USENIX Security）

## 1) 目标重塑：从“合规审计工具”到“AI Safety 科学问题”

**核心主张（claim）**
- 现有 agent safety 系统几乎都偏“阻断（blocking）”，但缺少“可验证的根因解释（verifiable causal explanation）”。
- 仅有阻断不足以支持事故复盘、策略改进与监管问责。
- CausalAudit 提供的是：
  1. 形式化违规定义；
  2. 可计算的最小反事实修复；
  3. 对解释“正确性/最小性/可执行性”的定量评测。

**一句话版本（可放摘要）**
> We formulate agent safety auditing as a constrained counterfactual search problem over execution traces, and show that minimal, policy-grounded counterfactuals yield faithful and actionable explanations beyond prevention-only monitors.

---

## 2) 顶会可发表的“硬贡献”清单（必须至少做到 3 项）

### C1. 形式化问题定义 + 可证明性质
把问题写成：
- 输入：trace `T`、policy `P`、语义约束 `S`。
- 输出：最小编辑 `Δ*`，使 `Δ*(T)` 合规且语义有效。

建议给出 2 个理论结果（哪怕是简化版）：
1. **复杂度结论**：最小编辑求解是 NP-hard（可由最小修复/规划问题归约）。
2. **可计算保证**：在限定 policy 片段（如单调时序 + 有限窗口）下，算法有多项式上界或近似比。

### C2. 不是“提示词工程”的算法核心
至少实现两套可对比算法：
1. **Exact/Optimal**：ILP 或 SAT/SMT 编码，求全局最小编辑。
2. **Fast/Approx**：启发式束搜索（beam search）+ policy-guided pruning。

并展示：
- 精确法质量高但慢；
- 近似法速度快且质量接近。

### C3. 新 benchmark（这是顶会关键）
构建 **CausalAudit-Bench**：
- 覆盖三类策略：授权、信息流、时序约束；
- 每条违规样本给出：违规事件、证据链、最小修复 gold。
- 包含单智能体 + 多智能体（消息传播导致违规）。

最低目标：
- 300 条起步（pilot），最终 1k+ 更有竞争力。
- 公开生成脚本、标注协议、一致性指标（Cohen’s kappa）。

### C4. 新评测指标（不仅是 precision/recall）
加入 explanation 专属指标：
- **Causal Faithfulness**：删除预测根因后违规是否消失；
- **Minimality Gap**：预测编辑长度与最优编辑长度差距；
- **Actionability**：修复后任务成功率保持程度；
- **Human Audit Utility**：审计员任务时间/正确率提升。

### C5. 强基线与消融
必须包含：
- prevention-only monitor（PCAS 类）
- LLM-judge（闭源与开源各一个）
- first-hit / random / nearest-template
- 去掉 IR、去掉语义约束、去掉 taint propagation 的消融

---

## 3) 论文结构（顶会叙事模板）

1. **Motivation**：安全事故复盘缺“根因+修复”
2. **Problem**：定义最小反事实审计问题
3. **Method**：Policy IR + checker + counterfactual solver
4. **Theory**：复杂度与可计算边界
5. **Benchmark**：数据构建协议与质量控制
6. **Experiments**：有效性、效率、泛化、人评
7. **Case Studies**：真实世界 agent 违规链路
8. **Limitations & Ethics**：误导性解释、策略歧义、责任边界

---

## 4) 8 个月可执行路线（按顶会倒排）

### M1-M2：问题与系统最小闭环
- 完成形式化定义、Policy IR v1、checker v1。
- 产出 50 条手工样本 + 失败案例集。

### M3-M4：算法与可证明部分
- 实现 ILP/SMT 精确求解器。
- 实现 beam + pruning 近似求解器。
- 给出复杂度命题与证明草稿。

### M5：Benchmark v1
- 自动注入违规脚本、标注工具链、IAA（标注一致性）评估。
- 发布 300 条版本，内部 ablation 全跑通。

### M6：大规模实验
- 扩到 1k 条，补多智能体场景。
- 加入人类审计小实验（n=12~20 即可做 pilot）。

### M7：写作与补实验
- 完成主实验图表、case study、威胁与局限性章节。
- 补充负结果（何时反事实不稳定）。

### M8：投稿打磨
- 双盲清理、artifact 复现文档、开源包。
- 目标会议：CCS / IEEE S&P / USENIX Security（按截稿期选主投）。

---

## 5) 你现在就能做的“第一周任务清单”

1. 把当前 proposal 改成“研究问题 + 假设 + 可证性 + 可复现实验”结构。
2. 写出 10 条严格 policy（每类至少 3 条）。
3. 定义统一 trace JSON schema（含 taint 字段、事件依赖）。
4. 实现 checker baseline（先 deterministic，不依赖 LLM）。
5. 做 30 条 toy traces，验证三类违规都能定位。
6. 明确主指标与统计检验（bootstrap CI / paired test）。

---

## 6) 投稿风险与规避

### 风险 R1：被审稿人认为“只是工程整合”
- 对策：增加形式化与理论结果；给最优性/近似性分析。

### 风险 R2：数据集太小、标注主观
- 对策：公开协议、双人标注、报告一致性、放出生成器。

### 风险 R3：LLM 组件不稳定
- 对策：核心 checker/solver 不依赖 LLM；LLM 仅用于 NL→IR，可替换。

### 风险 R4：与已有 monitor 区分不够
- 对策：强调“explanation faithfulness + minimal repair”是新问题，不是阻断增强。

---

## 7) 可直接放在你题目/摘要里的改名建议

- **CausalAudit: Counterfactual Explanations for Agent Safety Violations**
- **CausalAudit: Verifiable Root-Cause and Minimal Repair for Unsafe Agent Behavior**
- **Beyond Blocking: Counterfactual Auditing of Tool-Using AI Agents**

---

## 8) 一句话定位（面试/答辩可直接背）

我做的不是传统系统防火墙，而是 AI agent safety 的“事后可验证审计层”：把违规从“被拦截了”提升到“可解释、可归因、可最小修复、可评测”。
