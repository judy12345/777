# CausalAudit: Counterfactual Auditing of Safety Violations in Tool-Using AI Agents

**Author:** Yuwei Han (draft by assistant collaboration)  
**Target venues:** ACM CCS / IEEE S&P / USENIX Security

## Abstract
Runtime safety monitors for LLM agents can block unsafe actions, yet they rarely provide forensic explanations that identify root causes and minimal repairs. We present **CausalAudit**, a trace-grounded framework that converts policy violations into a constrained counterfactual search problem. Given a violated trace and a structured Policy Intermediate Representation (Policy IR), CausalAudit returns (1) causal explanations via deletion-based root-cause edits, and (2) corrective explanations via insertion/replacement repairs. We implement a deterministic compliance checker with taint-aware information-flow reasoning and evaluate on a synthetic benchmark covering authorization, information flow, and sequential constraints.

## 1. Introduction
Tool-using AI agents now issue network requests, file operations, and delegated sub-agent calls. In regulated settings, post-incident auditing requires actionable root-cause reports. Existing prevention-oriented systems emphasize blocking but under-serve explanation. We argue that explanation should be modeled as **minimal trace repair** under policy semantics.

## 2. Problem Formulation
Let a trace be `T = (e1..en)` and policy be `P`. If `T` violates `P`, CausalAudit seeks a minimal edit `Δ*` such that `Δ*(T)` is policy-compliant and semantically valid. Edit primitives are delete, insert, and replace.

## 3. Method
### 3.1 Trace Schema
We model events with typed records (`UserMessage`, `ToolCall`, `FileAccess`, `NetworkRequest`, etc.) and metadata fields (`domain`, `tool_name`, `derived_from`, `payload_tag`).

### 3.2 Policy IR
Policy IR fields: action, condition, requirement, timing, exception, and family (`authorization`, `infoflow`, `sequential`).

### 3.3 Compliance Checker
The checker performs event filtering, condition matching, exception filtering, requirement timing checks, and taint propagation for infoflow.

### 3.4 Counterfactual Engine
Candidate edits are enumerated and ranked by semantic cost: delete < insert < replace. A candidate is accepted iff re-checking yields compliance.

## 4. Prototype Implementation
We release an MVP Python implementation with:
- Deterministic checker and evidence chains
- Cost-ranked counterfactual search
- Benchmark generation scripts
- End-to-end demo and unit tests

## 5. Evaluation Snapshot
On benchmark v0 (30 cases), the prototype currently achieves:
- Violation recall: 1.0
- Root-cause exact match: 1.0
- Corrective compliance rate: 1.0

These results validate pipeline correctness on controlled traces; larger stress tests and human audit studies remain future work.

## 6. Limitations and Ethics
The current benchmark is synthetic and policy scope is restricted to three families. Real deployments require richer semantics (cross-trace state, identity binding, partial observability) and human oversight to avoid over-trusting automatic explanations.

## 7. Conclusion
CausalAudit reframes agent safety auditing as counterfactual minimal repair. This complements blocking-based safety stacks and supports explainable, operationally actionable post-incident analysis.

## References (selected)
1. Ding et al., Policy Compiler for Secure Agentic Systems, 2026.
2. Poskitt et al., AgentSpec, ICSE 2026.
3. Wachter et al., Counterfactual Explanations, 2018.
4. Yao et al., ReAct, ICLR 2023.
