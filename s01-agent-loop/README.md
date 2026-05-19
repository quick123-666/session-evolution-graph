# s01 — Agent Loop：最小可运行

## 本章目标

理解 **Agent 循环**的本质：
- 用户消息 → 发给 LLM → 模型回复
- 判断是否要调用工具
- 是 → 执行工具，write-back 到 messages[]
- 否 → 返回文字，结束

## 核心代码（58 行）

```python
import json
from datetime import datetime

MESSAGES = []

def user_message(content: str) -> None:
    """追加用户消息"""
    MESSAGES.append({"role": "user", "content": content})

def call_model(messages: list, tools: list | None = None) -> dict:
    """
    发给 LLM（这里用 print 模拟）。
    真实场景: openai.chat.completions.create(...)
    """
    print(f"\n[模型收到 {len(messages)} 条消息]")
    prompt = "\n".join(m["content"] for m in messages)
    # 模拟模型回复：遇到 "问题" 就创建问题节点
    if "问题" in prompt and "创建" in prompt:
        return {
            "role": "assistant",
            "content": "已创建问题节点",
            "tool_use": None
        }
    return {"role": "assistant", "content": "请描述你要追踪的问题", "tool_use": None}

def execute_tool(tool_name: str, args: dict) -> str:
    """执行工具，返回结果"""
    if tool_name == "write_problem":
        problem = {
            "id": f"prob_{args['id']}",
            "title": args["title"],
            "status": "in_progress",
            "created_at": datetime.now().isoformat()
        }
        return json.dumps(problem, ensure_ascii=False)
    return "{}"

def run(user_input: str) -> str:
    """主循环"""
    user_message(user_input)
    while True:
        response = call_model(MESSAGES, tools=[])
        MESSAGES.append(response)
        if not response.get("tool_use"):
            return response["content"]
        tool_call = response["tool_use"]
        result = execute_tool(tool_call["name"], tool_call["args"])
        MESSAGES.append({"role": "tool", "content": result})

if __name__ == "__main__":
    result = run("创建一个问题：研究 n8n 工作流自动化")
    print(f"\n最终回复: {result}")
```

## motto

> **"循环本身不「想」，想的是模型；代码只负责执行模型点的工具、把结果喂回去。"**

## 本章新增概念

| 概念 | 说明 |
|------|------|
| `messages[]` | 对话历史，write-back 的载体 |
| `tool_use` | 模型决定调用哪个工具 |
| write-back | 把工具结果追加到 messages 再回传模型 |

## 下章预告

s02：在**不改变循环结构**的前提下，往「工具分发表」里加 `read_file`、`timeline_append` 等 Handler。

> **motto**: "加工具 = 加一个 handler，循环不变。"
