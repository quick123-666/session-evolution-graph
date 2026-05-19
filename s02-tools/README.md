# s02 — Tools：工具分发表

## 本章目标

在**不改变循环结构**的前提下，往「工具分发表」里加入多个 Handler。

## 核心增量（+30 行 vs s01）

s01 只有 `write_problem`。s02 新增：

- `read_problem` — 读取已有问题
- `timeline_append` — 追加时间线事件
- `search_problems` — 搜索问题列表

## motto

> **"加工具 = 加一个 handler，循环不变。"**

## 核心代码片段

```python
# 工具分发表（新增）
TOOL_HANDLERS = {
    "write_problem": handle_write_problem,
    "read_problem":  handle_read_problem,
    "timeline_append": handle_timeline_append,
    "search_problems": handle_search,
}

# 循环不变（仍是这三行）
response = call_model(messages, tools=list(TOOL_HANDLERS.keys()))
messages.append(response)
if response.get("tool_use"):
    result = TOOL_HANDLERS[response["tool_use"]["name"]](response["tool_use"]["args"])
    messages.append({"role": "tool", "content": result})
```

## 下章预告

s03：引入 Todo 列表 — 让模型**先计划再执行**，避免边做边忘。

> **motto**: "一个没有计划的 Agent 会漂泊（drifts）。"
