"""
s02 — Tools：图谱写入层

Motto: "加工具 = 加一个 handler，循环不变。"

┌─────────────────────────────────────────────────────────────┐
│  s01 新增：write_problem（写入问题节点）                    │
│  s02 新增：add_child_problem（创建父子演化关系）            │
│  ─────────────────────────────────────────────             │
│  循环结构完全不变，工具表变长                                │
└─────────────────────────────────────────────────────────────┘

本章增量（vs s01）：
    - add_child_problem 工具（创建演化边 → problem_evolution 表）
    - 问题节点 + 演化边 同时写入
    - 工具分发表：TOOL_HANDLERS

数据模拟（脱敏）：
    - problem_tracking（节点）
    - problem_evolution（边：parent → child）
"""

import json
from datetime import datetime

# ── 模拟数据库 ────────────────────────────────────────────────
PROBLEMS:     list[dict] = []  # problem_tracking
EVOLUTIONS:   list[dict] = []  # problem_evolution
CALL_COUNT    = 0

# ── 工具分发表（核心新增）─────────────────────────────────────
def tool_write_problem(args: dict) -> str:
    """写入一个问题节点"""
    problem = {
        "id":                args["id"],
        "title":             args["title"],
        "stage":             args.get("stage", "explore"),
        "status":            "open",
        "first_observed_at": datetime.now().isoformat(),
    }
    PROBLEMS.append(problem)
    return json.dumps({"ok": True, "problem": problem}, ensure_ascii=False)

def tool_add_child_problem(args: dict) -> str:
    """
    创建父子演化关系（边）
    → 写入 problem_evolution 表
    """
    evolution = {
        "id":                f"pe_{len(EVOLUTIONS)+1:04d}",
        "parent_problem_id": args["parent_id"],
        "child_problem_id":  args["child_id"],
        "evolution_type":     args.get("type", "derived"),
        "description":        args.get("description", "问题细化"),
        "created_at":         datetime.now().isoformat(),
    }
    EVOLUTIONS.append(evolution)

    # 同步更新子问题的 stage
    for p in PROBLEMS:
        if p["id"] == args["child_id"]:
            p["derived_from"] = args["parent_id"]
            break

    return json.dumps({"ok": True, "evolution": evolution}, ensure_ascii=False)

TOOL_HANDLERS = {
    "write_problem":     tool_write_problem,
    "add_child_problem": tool_add_child_problem,
}

# ── LLM 调用（确定性模拟）────────────────────────────────────
def call_llm(messages: list[dict]) -> dict:
    """
    模拟 LLM 三轮决策：
      1. 识别父问题，写入 problem_tracking
      2. 识别子问题，写入 problem_tracking
      3. 建立父子关系，写入 problem_evolution
      4. 返回完成
    """
    global CALL_COUNT
    CALL_COUNT += 1
    prompt = "\n".join((m["content"] or "") for m in messages)
    print(f"  [LLM 第{CALL_COUNT}轮] 收到 {len(messages)} 条消息")

    # 第1轮：识别父问题
    if CALL_COUNT == 1:
        return {
            "role": "assistant", "content": None,
            "tool_use": {
                "name": "write_problem",
                "args": {"id": "prob_0001", "title": "Claude Code 会话超时断开", "stage": "explore"}
            }
        }

    # 第2轮：识别子问题
    if CALL_COUNT == 2:
        return {
            "role": "assistant", "content": None,
            "tool_use": {
                "name": "write_problem",
                "args": {"id": "prob_0002", "title": "Windows 长任务断连问题", "stage": "expand"}
            }
        }

    # 第3轮：建立父子关系
    if CALL_COUNT == 3:
        return {
            "role": "assistant", "content": None,
            "tool_use": {
                "name": "add_child_problem",
                "args": {
                    "parent_id":  "prob_0001",
                    "child_id":   "prob_0002",
                    "type":       "derived",
                    "description": "细化：具体到 Windows 平台的断连场景",
                }
            }
        }

    # 第4轮：无 tool_use，结束
    return {"role": "assistant", "content": "已完成节点和边的写入", "tool_use": None}

# ── 主循环（与 s01 完全相同）─────────────────────────────────
def run(user_message: str) -> str:
    global CALL_COUNT
    CALL_COUNT = 0
    messages = [{"role": "user", "content": user_message}]

    print(f"\n{'='*56}")
    print("Session Evolution Graph | s02 — 图谱写入层：节点 + 演化边")
    print(f"{'='*56}")

    while True:
        response = call_llm(messages)
        messages.append(response)

        if not response.get("tool_use"):
            print(f"\n[最终回复] {response['content']}")
            return response["content"]

        tool_name = response["tool_use"]["name"]
        tool_args = response["tool_use"]["args"]
        print(f"  >> 执行工具: {tool_name}")
        result = TOOL_HANDLERS[tool_name](tool_args)
        print(f"  << 工具返回: {result}")

        messages.append({"role": "tool", "content": result})  # write-back

    return messages[-1]["content"]

# ── 入口 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    run("用户反馈 Claude Code 在 Windows 下执行长任务时会话超时断开，"
        "进一步发现是 Windows 平台特有的长连接保持问题")

    print(f"\n{'─'*56}")
    print("【problem_tracking 表】")
    for p in PROBLEMS:
        print(f"  [{p['id']}] {p['title']} | stage={p['stage']} | derived_from={p.get('derived_from', '-')}")

    print(f"\n【problem_evolution 表】")
    for e in EVOLUTIONS:
        print(f"  [{e['id']}] {e['parent_problem_id']} --{e['evolution_type']}--> {e['child_problem_id']}")
        print(f"         说明: {e['description']}")
