<div align="center">

# Session Evolution Graph

### 会话演化图谱 · 从对话里长出问题图谱的 Agent 教学实验室

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![语言](https://img.shields.io/badge/文档-中英双语-red)](README.md)
[![Chapters](https://img.shields.io/badge/Chapters-s01%E2%80%93s03-orange)](./s01-agent-loop/)
[![GraphSpec](https://img.shields.io/badge/Spec-GraphSpec-purple)](./assets/GraphSpec-Paper.md)

**[中文说明](#目录)** · **[English](#english)** · [架构文档](./docs/session-extraction.md) · [GraphSpec](./assets/GraphSpec-Paper.md)

**模型是司机，Harness 是车，演化图谱是会话的地图。**

*The model drives. The harness is the vehicle. The evolution graph is the map of the conversation.*

![架构示意：Session → s01 提炼 → s02 图谱 → s03 查询](./assets/architecture-overview.svg)

</div>

---

## 目录

- [这是什么](#这是什么)
- [解决什么问题](#解决什么问题)
- [核心特性](#核心特性)
- [系统架构](#系统架构)
- [三章课程](#三章课程)
- [快速开始](#快速开始)
- [数据模型](#数据模型)
- [工具一览](#工具一览)
- [示例输出](#示例输出)
- [设计原则](#设计原则)
- [与相关项目的关系](#与相关项目的关系)
- [路线图](#路线图)
- [贡献](#贡献)
- [许可证](#许可证)
- [GitHub 展示：Pin / Topics](#github-展示pin--topics)
- [English 英文说明](#english)

---

## 这是什么

**Session Evolution Graph（会话演化图谱）** 是一个**从零搭建 Agent Harness** 的教学仓库，专注一件事：

> 把日常 AI 对话（Session）自动提炼成可查询的**问题演化图谱**（Evolution Graph）。

不是又一个 ChatGPT 套壳，而是可运行的 **Python 实验课**（s01 → s03）：每章只增加一层机制，让你看清「循环 → 工具 → 计划 → 图谱读写」如何拼装成完整系统。

| 三个词 | 含义 |
|--------|------|
| **Session（会话）** | `Messages[]` 是对话源流，图谱的数据来源 |
| **Evolution（演化）** | 问题之间 `derived`（细化）/ `solved`（解决）的父子关系 |
| **Graph（图谱）** | `problem_tracking`（节点）+ `problem_evolution`（边） |

---

## 解决什么问题

| 痛点 | 本仓库的做法 |
|------|----------------|
| 聊了很多，事后想不起「讨论过哪些问题」 | 从会话提炼 **Problem 节点** |
| 问题越聊越细，关系理不清 | 写入 **演化边**，形成链条 |
| Agent 教程太抽象，看不懂和业务的连接 | 每章 ~150 行可运行代码 + 明确图谱语义 |
| 想对齐 GraphForge / GraphSpec | 数据模型与 [GraphSpec](./assets/GraphSpec-Paper.md) 一致 |

---

## 核心特性

- **分章增量**：s01 只有循环，s02 加边，s03 加计划与查询 —— diff 即课件  
- **图谱优先**：工具命名与表结构围绕 `problem_tracking` / `problem_evolution`  
- **Harness 教学法**：对齐 [Learn Claude Code](https://learn.shareai.run/en/) 的「一层一课」  
- **零依赖演示**：`python agent.py` 即可跑通（LLM 为确定性模拟，便于理解 write-back）  
- **可扩展**：替换 `call_llm()` 即可接 OpenAI / Claude / Ollama；内存表可换 Supabase  

---

## 系统架构

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Session    │     │  s01 提炼层   │     │  s02 图谱层   │     │  s03 查询层   │
│  会话消息流  │────▶│ write_problem │────▶│ + evolution  │────▶│ get_chain    │
└─────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

详细 Mermaid 图与提炼判断逻辑见 **[docs/session-extraction.md](./docs/session-extraction.md)**（中文架构文档）。

---

## 三章课程

| 章节 | 目录 | 图谱角色 | 新增能力 | Motto |
|------|------|----------|----------|-------|
| **s01** | [`s01-agent-loop/`](./s01-agent-loop/) | 提炼层 | Agent 循环 + `write_problem` | 循环本身不「想」，想的是模型 |
| **s02** | [`s02-tools/`](./s02-tools/) | 写入层 | `add_child_problem` 演化边 | 加工具 = 加一个 handler，循环不变 |
| **s03** | [`s03-planning/`](./s03-planning/) | 查询层 | Todo + `get_evolution_chain` | 没有计划的 Agent 会漂泊 |

### Agent 核心循环（全书不变）

```python
while True:
    response = call_llm(messages)          # 发给大模型
    messages.append(response)
    if not response.get("tool_use"):
        return response["content"]        # 无工具调用 → 结束
    result = TOOL_HANDLERS[name](args)    # 执行工具
    messages.append({"role": "tool", "content": result})  # write-back 写回
```

---

## 快速开始

### 环境要求

- Python **3.10+**
- 无需安装第三方包（当前章节为教学模拟）

### 克隆与运行

```bash
git clone https://github.com/quick123-666/session-evolution-graph.git
cd session-evolution-graph

# 第 1 章：会话 → 问题节点
python s01-agent-loop/agent.py

# 第 2 章：节点 + 父子演化边
python s02-tools/agent.py

# 第 3 章：计划 + 演化链查询
python s03-planning/agent.py
```

> [!TIP]
> Windows 终端若中文乱码，可先执行：`$env:PYTHONIOENCODING='utf-8'`

### 推荐学习顺序

1. 读 [`s01-agent-loop/README.md`](./s01-agent-loop/README.md)，跑 `agent.py`  
2. 对比 s01 / s02 / s03 的 `agent.py` diff，只看**新增工具**  
3. 读 [`docs/session-extraction.md`](./docs/session-extraction.md) 理解三层架构  
4. （进阶）将 `call_llm` 换成真实 API，把 `PROBLEMS` 接到 Supabase  

---

## 数据模型

### 节点表 `problem_tracking`（问题追踪）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 如 `prob_0001` |
| `title` | string | 问题简称 |
| `stage` | enum | 阶段：`explore` 探索 / `expand` 展开 / `resolve` 解决 |
| `status` | enum | 状态：`open` 进行中 / `resolved` 已解决 |
| `first_observed_at` | datetime | 首次从会话中发现的时间 |
| `derived_from` | string? | 父问题 ID（便于链式查询） |

```json
{
  "id": "prob_0001",
  "title": "Claude Code 会话超时断开",
  "stage": "explore",
  "status": "open",
  "first_observed_at": "2026-05-19T10:00:00"
}
```

### 边表 `problem_evolution`（问题演化）

| 字段 | 类型 | 说明 |
|------|------|------|
| `parent_problem_id` | string | 父节点 |
| `child_problem_id` | string | 子节点 |
| `evolution_type` | enum | `derived` 细化 / `solved` 解决 |
| `description` | string | 关系说明 |

```json
{
  "parent_problem_id": "prob_0001",
  "child_problem_id": "prob_0002",
  "evolution_type": "derived",
  "description": "细化：Windows 平台长任务断连"
}
```

---

## 工具一览

| 工具 | 章节 | 读/写 | 作用 |
|------|------|-------|------|
| `write_problem` | s01 | 写 | 从会话识别并创建问题节点 |
| `add_child_problem` | s02 | 写 | 建立父子演化关系 |
| `todo_write` / `todo_done` | s03 | 写 | 先计划再执行 |
| `get_problem` | s03 | 读 | 按 ID 查节点 |
| `get_evolution_chain` | s03 | 读 | 查完整演化链 |
| `get_all_problems` | s03 | 读 | 按 status / stage 过滤 |

---

## 示例输出

**s02 运行后**（节点 + 边）：

```text
【problem_tracking 问题节点表】
  [prob_0001] Claude Code 会话超时断开 | stage=explore
  [prob_0002] Windows 长任务断连问题   | stage=expand | derived_from=prob_0001

【problem_evolution 演化关系表】
  [pe_0001] prob_0001 --derived--> prob_0002
```

**s03 运行后**（演化链查询）：

```text
[prob_0001] Claude Code 会话超时断开 (explore/open)
  -> [prob_0002] Windows 长任务断连问题 (expand/open)
    -> [prob_0003] Session 超时机制需要延长 (resolve/resolved)
```

---

## 设计原则

1. **图谱不是手动画的** —— 应从 Session 持续提炼，而非一次性导入  
2. **聪明在模型，工程在 Harness** —— 代码负责工具、权限、上下文，不堆假智能  
3. **循环稳定，工具增长** —— 与 [Learn Claude Code](https://learn.shareai.run/en/) 同构  
4. **对齐 GraphSpec** —— 节点/边/阶段命名与 GraphForge 生态一致  

> [!NOTE]
> 当前 `call_llm()` 为**确定性模拟**（按轮次触发工具），用于教学。生产环境请替换为真实 LLM，并增加幂等、鉴权与审计。

---

## 与相关项目的关系

| 项目 | 关系 |
|------|------|
| [Learn Claude Code](https://learn.shareai.run/en/) | 通用 Harness 教学法；本仓库是其「图谱专题课」 |
| [GraphSpec / GraphForge](./assets/GraphSpec-Paper.md) | 数据规范参考 |
| [star-level](https://github.com/quick123-666/star-level) | 同作者的 Next.js 全栈示例 |
| [bounded-memory](https://github.com/quick123-666/bounded-memory) | 同作者的 AI 记忆系统 |

---

## 路线图

- [x] s01 — Agent 循环 + 问题节点写入  
- [x] s02 — 演化边 `add_child_problem`  
- [x] s03 — Todo 计划 + 图谱查询  
- [ ] s04 — 持久化（JSON / Supabase）  
- [ ] s05 — 真实 LLM 接入（OpenAI 兼容 API）  
- [ ] s06 — 从 Cursor / Claude Code 会话日志自动导入  
- [ ] 可视化：演化链前端（Mermaid / D3）  

欢迎通过 [Issue](https://github.com/quick123-666/session-evolution-graph/issues) 讨论需求。

---

## 贡献

1. Fork 本仓库  
2. 创建分支：`git checkout -b feature/your-idea`  
3. 提交改动：`git commit -m "feat: 描述你的改动"`  
4. 推送并发起 Pull Request  

小步提交、清晰 commit message，与课程精神一致。

---

## 许可证

本项目采用 [MIT License](./LICENSE) 开源。

---

## GitHub 展示：Pin / Topics

| 操作 | 说明 |
|------|------|
| **Pin 到个人主页** | 在 [你的主页](https://github.com/quick123-666) 点 **Customize your pins**，把本仓库固定到最上方（最多 6 个） |
| **Topics 标签** | 仓库 **About → Edit**，建议添加：`agent` `llm` `knowledge-graph` `python` `graphspec` `evolution-graph` |
| **详细图文步骤** | 见 [docs/github-展示设置.md](./docs/github-展示设置.md) |

---

<a id="english"></a>

## English

### Overview

**Session Evolution Graph** is a hands-on course for building an **Agent harness** that turns LLM conversations into a queryable **evolution graph** of problems (`problem_tracking` + `problem_evolution`).

### Quick Start

```bash
git clone https://github.com/quick123-666/session-evolution-graph.git
cd session-evolution-graph
python s01-agent-loop/agent.py
python s02-tools/agent.py
python s03-planning/agent.py
```

### Chapters

| Ch | Folder | Role |
|----|--------|------|
| s01 | [s01-agent-loop](./s01-agent-loop/) | Extract — `write_problem` |
| s02 | [s02-tools](./s02-tools/) | Graph write — `add_child_problem` |
| s03 | [s03-planning](./s03-planning/) | Plan & query — `get_evolution_chain` |

### Features

- Incremental chapters (loop → tools → query)  
- GraphSpec-aligned schema  
- Zero deps for teaching demos — swap `call_llm()` for production  
- Same harness pedagogy as [Learn Claude Code](https://learn.shareai.run/en/)  

### Roadmap

- [x] s01–s03 labs  
- [ ] s04 Supabase persistence  
- [ ] s05 real LLM API  
- [ ] s06 IDE session import  
- [ ] graph visualization UI  

### License

[MIT](./LICENSE)

---

<div align="center">

**如果对你有帮助，欢迎 Star / Star if helpful**

[quick123-666](https://github.com/quick123-666) · [报告问题 / Issues](https://github.com/quick123-666/session-evolution-graph/issues)

</div>
