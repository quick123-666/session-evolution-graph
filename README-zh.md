# Session Evolution Graph · 会话演化图谱

**从会话提炼演化图谱的 Agent 教学课** — 节点、边、演化链，从对话里长出来。

> Motto: *模型是司机，Harness 是车；演化图谱是会话的地图。*

| 关键词 | 含义 |
|--------|------|
| **Session** | 日常对话 `Messages[]` 是图谱的数据源 |
| **Evolution** | 问题之间的 `derived` / `solved` 演化关系 |
| **Graph** | `problem_tracking` 节点 + `problem_evolution` 边 |

---

## 课程结构

```
session-evolution-graph/
├── README-zh.md
├── docs/
│   └── session-extraction.md    ← 图谱三层架构（提炼 / 写入 / 查询）
├── assets/
│   └── GraphSpec-Paper.md       ← GraphSpec 规范摘要
├── s01-agent-loop/              ← 提炼层：识别问题节点
├── s02-tools/                   ← 图谱层：节点 + 演化边
└── s03-planning/                ← 查询层：计划 + 演化链查询
```

---

## 三章增量

| 章节 | 图谱角色 | 新增工具 | Motto |
|------|----------|----------|-------|
| s01 | **提炼层** | `write_problem` | 循环本身不「想」，想的是模型 |
| s02 | **图谱写入层** | `add_child_problem` | 加工具 = 加一个 handler，循环不变 |
| s03 | **查询层** | `get_evolution_chain` 等 | 一个没有计划的 Agent 会漂泊 |

---

## 数据模型（图谱核心）

### 节点 — `problem_tracking`

```python
{"id": "prob_0001", "title": "...", "stage": "explore", "status": "open"}
```

### 边 — `problem_evolution`

```python
{"parent_problem_id": "prob_0001", "child_problem_id": "prob_0002", "evolution_type": "derived"}
```

### 查询 — 演化链

```python
{"chain": [prob_0001 → prob_0002 → prob_0003], "depth": 3}
```

---

## 快速运行

```bash
python s01-agent-loop/agent.py   # 提炼：会话 → 问题节点
python s02-tools/agent.py        # 写入：节点 + 演化边
python s03-planning/agent.py     # 查询：演化链 + 过滤列表
```

---

## 核心观点

1. **演化图谱不是手动画出来的**，是从会话里持续提炼的  
2. **工程师做 Harness**：写工具、查图谱、管计划  
3. **模型是司机，Harness 是车，演化图谱是地图**  
4. 规范对齐 **GraphSpec**（见 `assets/GraphSpec-Paper.md`）

---

## 参考

- [Learn Claude Code](https://learn.shareai.run/en/) — 同类 Harness 教学法  
- `docs/session-extraction.md` — Mermaid 架构图与提炼逻辑  
