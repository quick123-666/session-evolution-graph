# s03 — Planning：计划结构

## 本章目标

引入 **Todo 列表**，让模型先计划再执行，避免边做边忘、反复横跳。

## 核心增量（+40 行 vs s02）

s02 只有工具调用。s03 新增：

- `todo_write` — 模型先写出步骤列表
- `todo_read` — 模型读取当前进度
- `todo_done` — 标记步骤完成

## motto

> **"一个没有计划的 Agent 会漂泊（An agent without a plan drifts）。"**

## 真实案例（GraphForge 演化链）

```
[问题] 研究 n8n 工作流自动化
  ↓ derived
[问题] 研究 MCP Protocol
  ↓ derived
[问题] 研究 Coding Agent 生态
  ↓ derived
[问题] 深入 Cursor IDE + agent-skills-hub
```

这本身就是一种**可见计划结构**——衍生链就是执行步骤。

## 下章预告

s04：引入子 Agent — 独立 messages[]，防上下文污染。

> **motto**: "子 Agent 有自己的记忆，不干扰父 Agent。"
