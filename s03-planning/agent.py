"""
s03 — Planning & Query：计划层 + 图谱查询层

Motto: "一个没有计划的 Agent 会漂泊。"
Motto: "图谱即查询结果。"

┌─────────────────────────────────────────────────────────────┐
│  s01: write_problem（节点写入）                              │
│  s02: add_child_problem（边写入）                           │
│  s03: plan + query（图谱查询）                              │
│  ─────────────────────────────────────────────             │
│  先制定计划，再按计划查询，逐步完成                           │
└─────────────────────────────────────────────────────────────┘

本章增量（vs s02）：
    - todo_write / todo_done 工具（计划结构）
    - get_problem / get_evolution_chain / get_all_problems 工具（图谱查询）
    - 模型必须先计划，再执行，最后返回查询结果

数据模拟（脱敏）：
    - 查询结果即为图谱的可视化状态
"""

import json
from datetime import datetime

# ── 预置数据（模拟已写入的图谱）───────────────────────────────
PROBLEMS:   list[dict] = [
    {"id": "prob_0001", "title": "Claude Code 会话超时断开",      "stage": "explore", "status": "open",    "first_observed_at": "2026-05-15T10:00:00"},
    {"id": "prob_0002", "title": "Windows 长任务断连问题",          "stage": "expand",  "status": "open",    "first_observed_at": "2026-05-15T11:00:00", "derived_from": "prob_0001"},
    {"id": "prob_0003", "title": "Session 超时机制需要延长",        "stage": "resolve", "status": "resolved", "first_observed_at": "2026-05-15T12:00:00", "derived_from": "prob_0002"},
    {"id": "prob_0004", "title": "Cursor IDE 子文件夹代理问题",     "stage": "explore", "status": "open",    "first_observed_at": "2026-05-16T09:00:00"},
]
EVOLUTIONS: list[dict] = [
    {"id": "pe_0001", "parent_problem_id": "prob_0001", "child_problem_id": "prob_0002", "evolution_type": "derived", "description": "细化：Windows 平台断连场景"},
    {"id": "pe_0002", "parent_problem_id": "prob_0002", "child_problem_id": "prob_0003", "evolution_type": "solved",   "description": "解决：超时机制优化"},
]

# ── 工具分发表 ────────────────────────────────────────────────
TODOS: list[dict] = []
CALL_COUNT = 0

def tool_todo_write(args: dict) -> str:
    """制定计划：写入 Todo 列表"""
    global TODOS
    TODOS = [
        {"id": i+1, "content": step, "status": "pending"}
        for i, step in enumerate(args.get("steps", []))
    ]
    return json.dumps({"ok": True, "todos": TODOS}, ensure_ascii=False)

def tool_todo_done(args: dict) -> str:
    """标记某步骤完成"""
    for t in TODOS:
        if t["id"] == args.get("id"):
            t["status"] = "done"
            t["done_at"] = datetime.now().isoformat()
    return json.dumps({"ok": True, "todos": TODOS}, ensure_ascii=False)

def tool_get_problem(args: dict) -> str:
    """按 ID 查询单个问题节点"""
    for p in PROBLEMS:
        if p["id"] == args.get("id"):
            return json.dumps({"ok": True, "problem": p}, ensure_ascii=False)
    return json.dumps({"ok": False, "error": f"问题 {args.get('id')} 不存在"})

def tool_get_evolution_chain(args: dict) -> str:
    """
    查询某个问题的完整演化链条（向上追父，向下追子）
    → 返回从根到叶的顺序列表
    """
    target = args.get("problem_id")
    chain = []
    visited = set()

    # 向上追父
    current = target
    while current:
        for p in PROBLEMS:
            if p["id"] == current:
                chain.insert(0, p)
                visited.add(current)
                current = p.get("derived_from")
                break
        else:
            break

    return json.dumps({
        "ok": True,
        "chain": [
            {"id": p["id"], "title": p["title"], "stage": p["stage"], "status": p["status"]}
            for p in chain
        ],
        "depth": len(chain),
    }, ensure_ascii=False)

def tool_get_all_problems(args: dict) -> str:
    """查询所有问题，支持按 status / stage 过滤"""
    status = args.get("status")
    stage  = args.get("stage")
    filtered = PROBLEMS
    if status:
        filtered = [p for p in filtered if p.get("status") == status]
    if stage:
        filtered = [p for p in filtered if p.get("stage") == stage]
    return json.dumps({
        "ok": True,
        "problems": filtered,
        "total": len(filtered),
    }, ensure_ascii=False)

TOOL_HANDLERS = {
    "todo_write":          tool_todo_write,
    "todo_done":           tool_todo_done,
    "get_problem":         tool_get_problem,
    "get_evolution_chain": tool_get_evolution_chain,
    "get_all_problems":   tool_get_all_problems,
}

# ── LLM 调用（确定性模拟）────────────────────────────────────
def call_llm(messages: list[dict]) -> dict:
    """
    模拟 LLM 四轮决策（先计划，再执行）：
      1. todo_write：制定查询计划
      2. get_evolution_chain：查演化链条
      3. todo_done：标记步骤完成
      4. 返回查询结果
    """
    global CALL_COUNT
    CALL_COUNT += 1
    print(f"  [LLM 第{CALL_COUNT}轮] 收到 {len(messages)} 条消息")

    if CALL_COUNT == 1:
        return {
            "role": "assistant", "content": None,
            "tool_use": {
                "name": "todo_write",
                "args": {"steps": [
                    "查询 prob_0001 的完整演化链条",
                    "查看所有 open 状态的问题",
                ]}
            }
        }

    if CALL_COUNT == 2:
        return {
            "role": "assistant", "content": None,
            "tool_use": {
                "name": "get_evolution_chain",
                "args": {"problem_id": "prob_0001"}
            }
        }

    if CALL_COUNT == 3:
        return {
            "role": "assistant", "content": None,
            "tool_use": {
                "name": "todo_done",
                "args": {"id": 1}
            }
        }

    return {"role": "assistant", "content": "查询完成", "tool_use": None}

# ── 主循环 ───────────────────────────────────────────────────
def run(user_message: str) -> str:
    global CALL_COUNT
    CALL_COUNT = 0
    messages = [{"role": "user", "content": user_message}]

    print(f"\n{'='*56}")
    print("Session Evolution Graph | s03 — 计划层 + 图谱查询层")
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

        messages.append({"role": "tool", "content": result})

    return messages[-1]["content"]

# ── 入口 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    run("查询问题图谱：了解当前所有 open 问题的演化状态")

    print(f"\n{'─'*56}")
    print("【演化链条：prob_0001】")
    chain_result = json.loads(tool_get_evolution_chain({"problem_id": "prob_0001"}))
    for i, node in enumerate(chain_result["chain"]):
        arrow = " -> " if i < len(chain_result["chain"]) - 1 else "    "
        print(f"  {'  ' * i}{arrow}[{node['id']}] {node['title']} ({node['stage']}/{node['status']})")

    print(f"\n【所有 open 问题】")
    all_result = json.loads(tool_get_all_problems({"status": "open"}))
    for p in all_result["problems"]:
        print(f"  [{p['id']}] {p['title']} | {p['stage']}")
