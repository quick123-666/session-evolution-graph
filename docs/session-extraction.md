# 从会话提炼图谱 · Session Evolution Graph

**核心观点**：图谱不是手动建的，是从日常会话里「长」出来的。

---

## 整体架构

```mermaid
flowchart TD
    subgraph 会话层
        C[用户会话流<br/>Messages List]
    end

    subgraph 提炼层["s01 — 提炼层"]
        E[提炼引擎<br/>Extract Engine]
    end

    subgraph 写入层["s02 — 图谱写入层"]
        N[问题节点<br/>write_problem]
        R[演化边<br/>add_child_problem]
    end

    subgraph 查询层["s03 — 计划 + 查询层"]
        Q[图谱查询<br/>get_evolution_chain]
    end

    C --> E
    E --> N
    E --> R
    N --> Q
    R --> Q

    style E fill:#e1f5fe
    style N fill:#c8e6c9
    style R fill:#ffe0b2
    style Q fill:#fff3e0
```

---

## 三层职责

| 层 | 做什么 | 输入→输出 |
|---|---|---|
| **提炼层（s01）** | 从会话里识别「问题」 | `Messages[]` → `write_problem` |
| **图谱写入层（s02）** | 写入问题节点 + 演化边 | `add_child_problem` → `problem_evolution` |
| **计划+查询层（s03）** | 先计划再查询，返回图谱状态 | `get_evolution_chain` → 链条视图 |

---

## 每章工具一览

| 章节 | 工具名 | 写入表 |
|---|---|---|
| s01 | `write_problem` | `problem_tracking` |
| s02 | `add_child_problem` | `problem_evolution` |
| s03 | `get_problem` | —（读） |
| s03 | `get_evolution_chain` | —（读） |
| s03 | `get_all_problems` | —（读） |

---

## 数据库两张表

### problem_tracking — 问题节点表

| 字段 | 含义 |
|---|---|
| `id` | 节点唯一标识 |
| `problem_title` | 问题简称 |
| `stage` | 当前阶段：`explore` / `expand` / `resolve` |
| `status` | 状态：`open` / `resolved` |
| `first_observed_at` | 首次发现时间 |
| `derived_from` | 父问题 ID（可选） |

### problem_evolution — 演化关系表

| 字段 | 含义 |
|---|---|
| `parent_problem_id` | 父问题 |
| `child_problem_id` | 子问题 |
| `evolution_type` | `derived`（细化）/ `solved`（解决） |
| `description` | 关系描述 |

---

## 提炼引擎的内部判断逻辑

```mermaid
flowchart LR
    Q1{会话提到<br/>未见过的问题?}
    Q2{该问题是之前<br/>问题的细化?}
    Q3{该问题<br/>已被解决?}

    Q1 -->|是| N1[write_problem<br/>新建节点]
    Q1 -->|否| N2[跳过]

    Q2 -->|是| N3[add_child_problem<br/>建演化边]
    Q2 -->|否| N4[write_problem<br/>独立节点]

    Q3 -->|是| N5[标记 resolved<br/>不建新边]
```

---

## Motto

> **「聪明」主要来自模型训练，不是你在 `if/else` 里堆出来的。**
> **工程师主要做的是 Harness（马甲）：工具、权限、上下文、知识加载、任务持久化。**
> **模型是司机，Harness 是车。**
> **图谱不是手动建的，是从会话里「长」出来的。**
