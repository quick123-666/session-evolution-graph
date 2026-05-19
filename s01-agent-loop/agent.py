"""
s01 — Agent Loop：提炼层 — 从会话识别问题节点

Motto: "循环本身不『想』，想的是模型；
        代码只负责执行模型点的工具、把结果喂回去。"

┌─────────────────────────────────────────────────────────────┐
│  用户消息 ──▶ 发给 LLM ──▶ 模型回复                        │
│                        │                                    │
│                  要不要调用工具？                             │
│                   /          \                              │
│                 是             否 ──▶ 返回用户，结束          │
│                 │                                                │
│          执行工具，把结果                                              │
│          追加到 messages[]                                       │
│                 │                                                │
│          回到开头（再问模型）                                     │
└─────────────────────────────────────────────────────────────┘

本章增量（vs 0）：
    - while True 主循环
    - write_problem 工具（写入问题节点）
    - write-back：把工具结果追加回 messages[]

数据模拟（脱敏）：
    - 问题节点表：problem_tracking（id, title, stage, status）
"""

import json
from datetime import datetime
from typing import Optional

# ── 模拟数据库（内存） ────────────────────────────────────────
PROBLEMS: list[dict] = []  # 模拟 problem_tracking 表

# ── 工具定义 ─────────────────────────────────────────────────
def tool_write_problem(args: dict) -> str:
    """写入一个问题节点到图谱"""
    problem = {
        "id": args["id"],
        "title": args["title"],
        "stage": args.get("stage", "explore"),
        "status": "open",
        "first_observed_at": datetime.now().isoformat(),
    }
    PROBLEMS.append(problem)
    return json.dumps({"ok": True, "problem": problem}, ensure_ascii=False)

TOOL_HANDLERS = {
    "write_problem": tool_write_problem,
}

TOOLS = [
    {
        "name": "write_problem",
        "description": "将识别到的问题写入图谱节点表",
        "parameters": {
            "type": "object",
            "properties": {
                "id":    {"type": "string", "description": "问题唯一标识"},
                "title": {"type": "string", "description": "问题简称"},
                "stage": {"type": "string", "enum": ["explore", "expand", "resolve"],
                          "description": "当前阶段"},
            },
            "required": ["id", "title"],
        },
    }
]

# ── LLM 调用（确定性模拟）────────────────────────────────────
CALL_COUNT = 0

def call_llm(messages: list[dict]) -> dict:
    """
    模拟 LLM 决策：
      - 第1轮：用户消息提到问题 → 触发 write_problem
      - 第2轮：无 tool_use → 返回文字，循环结束
    """
    global CALL_COUNT
    CALL_COUNT += 1
    prompt = "\n".join((m["content"] or "") for m in messages)
    print(f"  [LLM 第{CALL_COUNT}轮] 收到 {len(messages)} 条消息")

    # 第1轮：检测到问题，触发 write_problem
    if CALL_COUNT == 1:
        title = extract_title(prompt)
        return {
            "role": "assistant",
            "content": None,
            "tool_use": {
                "name": "write_problem",
                "args": {
                    "id":    f"prob_{len(PROBLEMS)+1:04d}",
                    "title": title,
                    "stage": "explore",
                }
            }
        }

    # 第2轮：问题已写入，返回结果
    return {"role": "assistant", "content": f"已识别并写入 {len(PROBLEMS)} 个问题节点", "tool_use": None}

def extract_title(prompt: str) -> str:
    """从用户消息里提取问题标题（简化逻辑）"""
    lines = [l.strip() for l in prompt.split("\n") if l.strip() and not l.startswith("[")]
    # 取第一行作为问题标题
    return lines[0] if lines else "未知问题"

# ── 主循环 ───────────────────────────────────────────────────
def run(user_message: str) -> str:
    """
    Agent 主循环：

        while True:
            response = call_llm(messages)
            messages.append(response)
            if not response.get("tool_use"):
                return response["content"]          # 结束
            result = TOOL_HANDLERS[response["tool_use"]["name"]](response["tool_use"]["args"])
            messages.append({"role": "tool", "content": result})  # ← write-back（最关键的一步）
    """
    global CALL_COUNT
    CALL_COUNT = 0
    messages = [{"role": "user", "content": user_message}]

    print(f"\n{'='*56}")
    print("Session Evolution Graph | s01 — 提炼层：从会话识别问题节点")
    print(f"{'='*56}")

    while True:
        response = call_llm(messages)
        messages.append(response)

        # 没有工具调用 → 返回结果，结束
        if not response.get("tool_use"):
            print(f"\n[最终回复] {response['content']}")
            return response["content"]

        # 执行工具
        tool_name = response["tool_use"]["name"]
        tool_args = response["tool_use"]["args"]
        print(f"  >> 执行工具: {tool_name}({tool_args.get('title', '')!r})")
        result = TOOL_HANDLERS[tool_name](tool_args)
        print(f"  << 工具返回: {result}")

        # write-back：把结果追加回 messages[]，模型继续「想」
        messages.append({"role": "tool", "content": result})

    return messages[-1]["content"]

# ── 入口 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run(
        "用户反馈：Claude Code 在 Windows 下执行 long-running 任务时会话超时断开"
    )
    print(f"\n{'─'*56}")
    print("已写入的问题节点（模拟 problem_tracking 表）：")
    for p in PROBLEMS:
        print(f"  [{p['id']}] {p['title']} | stage={p['stage']} | {p['status']}")
