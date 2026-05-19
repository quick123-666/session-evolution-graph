<div align="center">

# Session Evolution Graph

### Grow a problem evolution graph from AI chat sessions — an incremental Agent harness lab

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Chapters](https://img.shields.io/badge/Chapters-s01%E2%80%93s03-orange)](./s01-agent-loop/)
[![GraphSpec](https://img.shields.io/badge/Spec-GraphSpec-purple)](./assets/GraphSpec-Paper.md)

[中文说明](./README-zh.md) · [Architecture](./docs/session-extraction.md) · [GraphSpec](./assets/GraphSpec-Paper.md)

*The model drives. The harness is the vehicle. The evolution graph is the map of the conversation.*

</div>

---

## Table of Contents

- [Overview](#overview)
- [Problem](#problem)
- [Features](#features)
- [Architecture](#architecture)
- [Chapters](#chapters)
- [Quick Start](#quick-start)
- [Data Model](#data-model)
- [Tools](#tools)
- [Design Principles](#design-principles)
- [Related Projects](#related-projects)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Session Evolution Graph** is a hands-on course for building an **Agent harness** whose job is to turn everyday LLM conversations into a queryable **evolution graph** of problems:

- **Session** — `Messages[]` as the source stream  
- **Evolution** — parent/child links (`derived`, `solved`)  
- **Graph** — `problem_tracking` (nodes) + `problem_evolution` (edges)  

Each chapter (`s01` → `s03`) adds one mechanism only. Every step is runnable Python (~150 lines per chapter).

---

## Problem

| Pain point | This repo |
|------------|-----------|
| Long chats, no structured memory of "what we were solving" | Extract **Problem** nodes from sessions |
| Topics fork and deepen; relationships get lost | Persist **evolution edges** |
| Agent tutorials feel disconnected from real products | Code maps directly to graph tables |
| Need alignment with GraphForge / GraphSpec | Schema follows [GraphSpec](./assets/GraphSpec-Paper.md) |

---

## Features

- **Incremental chapters** — loop → tools → planning & query  
- **Graph-first tools** — `write_problem`, `add_child_problem`, `get_evolution_chain`  
- **Harness pedagogy** — same spirit as [Learn Claude Code](https://learn.shareai.run/en/)  
- **Zero third-party deps** for demos — swap `call_llm()` for production  
- **Extensible** — plug in OpenAI-compatible APIs and Supabase/Postgres  

---

## Architecture

```
Session (Messages[]) → s01 Extract → s02 Graph write → s03 Plan & query
```

See [docs/session-extraction.md](./docs/session-extraction.md) for Mermaid diagrams and extraction rules.

---

## Chapters

| Ch | Folder | Role | New tools |
|----|--------|------|-----------|
| s01 | [s01-agent-loop](./s01-agent-loop/) | Extract | `write_problem` |
| s02 | [s02-tools](./s02-tools/) | Graph write | `add_child_problem` |
| s03 | [s03-planning](./s03-planning/) | Query | `get_evolution_chain`, `todo_*` |

Core loop (unchanged across chapters):

```python
while True:
    response = call_llm(messages)
    messages.append(response)
    if not response.get("tool_use"):
        return response["content"]
    result = TOOL_HANDLERS[name](args)
    messages.append({"role": "tool", "content": result})
```

---

## Quick Start

```bash
git clone https://github.com/quick123-666/session-evolution-graph.git
cd session-evolution-graph

python s01-agent-loop/agent.py
python s02-tools/agent.py
python s03-planning/agent.py
```

Requirements: **Python 3.10+**, no pip install for the teaching demos.

> [!NOTE]
> `call_llm()` is a **deterministic simulator** for learning. Replace it with a real API for production.

---

## Data Model

**Nodes** (`problem_tracking`): `id`, `title`, `stage` (`explore` | `expand` | `resolve`), `status` (`open` | `resolved`)

**Edges** (`problem_evolution`): `parent_problem_id`, `child_problem_id`, `evolution_type` (`derived` | `solved`)

Full field tables: [README-zh.md](./README-zh.md#数据模型) (Chinese, more detail).

---

## Tools

| Tool | Chapter | R/W | Purpose |
|------|---------|-----|---------|
| `write_problem` | s01 | W | Create problem node from session |
| `add_child_problem` | s02 | W | Link parent → child |
| `todo_write` / `todo_done` | s03 | W | Plan before execute |
| `get_evolution_chain` | s03 | R | Full chain view |
| `get_all_problems` | s03 | R | Filter by status/stage |

---

## Design Principles

1. Graphs should **grow from sessions**, not manual one-off imports  
2. **Intelligence in the model, engineering in the harness**  
3. **Stable loop, growing tool table**  
4. **GraphSpec-aligned** naming and stages  

---

## Related Projects

- [Learn Claude Code](https://learn.shareai.run/en/) — general harness curriculum  
- [GraphSpec](./assets/GraphSpec-Paper.md) — schema reference  
- [star-level](https://github.com/quick123-666/star-level) — Next.js + Supabase app (same author)  
- [bounded-memory](https://github.com/quick123-666/bounded-memory) — lightweight AI memory  

---

## Roadmap

- [x] s01–s03 teaching labs  
- [ ] s04 persistence (Supabase)  
- [ ] s05 real LLM integration  
- [ ] s06 import from IDE session logs  
- [ ] Evolution graph visualization UI  

---

## Contributing

Fork → branch → PR. Small commits with clear messages match how this course is built.

---

## License

[MIT](./LICENSE)

---

<div align="center">

**Star the repo if this helps you build session → graph pipelines.**

[quick123-666](https://github.com/quick123-666) · [Issues](https://github.com/quick123-666/session-evolution-graph/issues)

</div>
