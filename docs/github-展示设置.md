# GitHub 展示设置：Pin、Topics、演示图

## 一、什么叫「Pin 到个人主页」？

你的 GitHub 主页是：**https://github.com/quick123-666**

别人点进去时，默认会看到 **Popular repositories（热门仓库）** 列表。  
**Pin（置顶）** = 你**手动选最多 6 个仓库**，固定显示在主页最上方，像「作品集橱窗」。

```
┌─────────────────────────────────────────┐
│  quick123-666  的个人主页                  │
├─────────────────────────────────────────┤
│  📌 Pinned（置顶，最多 6 个）              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ session- │ │ star-    │ │ bounded- │ │
│  │ evolution│ │ level    │ │ memory   │ │
│  └──────────┘ └──────────┘ └──────────┘ │
│  … 其余仓库在下面列表里 …                 │
└─────────────────────────────────────────┘
```

**为什么要 Pin？**  
访客 3 秒内能看到你最想展示的项目，而不是被 37 个仓库淹没。

### 操作步骤（约 30 秒）

1. 打开 https://github.com/quick123-666  
2. 右侧 **Pinned** 区域点 **Customize your pins**（自定义置顶）  
3. 勾选要展示的仓库，例如：  
   - `session-evolution-graph`  
   - `star-level`  
   - `bounded-memory`  
   - `code-memex-lite`  
   - `Claude-Bridge-claw`  
   - `network-backup-guardian`  
4. 拖拽调整顺序 → **Save**

> Pin 只影响**个人主页展示顺序**，不改变仓库本身。

---

## 二、什么叫 Topics（主题标签）？

**Topics** 是贴在**某个仓库**上的关键词，类似 B 站分区标签。

作用：

- 别人搜 `agent`、`knowledge-graph` 时更容易搜到你的仓库  
- 仓库标题下方会显示一排小标签，一眼看懂技术栈  

### 推荐为本仓库添加的 Topics

复制下面整行，到仓库 **About** 里粘贴（用逗号或回车分隔）：

```
agent, llm, knowledge-graph, python, graph, evolution-graph, graphspec, teaching, harness, session-memory
```

### 操作步骤

1. 打开 https://github.com/quick123-666/session-evolution-graph  
2. 右上角 **⚙️ About**（齿轮）→ **Edit repository details**  
3. **Description** 可填：  
   `从 AI 会话提炼问题演化图谱 · Agent 教学课（中英双语）`  
4. **Topics** 粘贴上面的标签  
5. **Save changes**

---

## 三、演示图是什么？放哪里？

**演示图** = README 里的一张架构图 / 运行截图，让人不读代码也能看懂项目。

本仓库已提供：

| 文件 | 用途 |
|------|------|
| [assets/architecture-overview.svg](../assets/architecture-overview.svg) | 三层架构示意图（README 顶部展示） |
| [docs/session-extraction.md](./session-extraction.md) | Mermaid 流程图（GitHub 自动渲染） |

以后可补充：

- `assets/demo-s01-output.png` — 运行 `s01/agent.py` 的终端截图  
- `assets/demo-evolution-chain.png` — s03 演化链输出截图  

截图后放进 `assets/`，在 README 里加：

```markdown
![运行示例](../assets/demo-s01-output.png)
```

---

## 四、和 Profile README 的区别

| 项目 | 是什么 |
|------|--------|
| **Profile README** | 仓库名 `quick123-666/quick123-666`，显示在主页**最顶部自我介绍** |
| **Pin 仓库** | 主页上**置顶的 6 个仓库卡片** |
| **仓库 README** | 点进 `session-evolution-graph` 后看到的说明（已中英双语） |
| **Topics** | 单个仓库的标签，在仓库名下方 |

四者配合效果最好：Profile 说你是谁 → Pin 展示代表作 → 仓库 README + 图说清项目。
