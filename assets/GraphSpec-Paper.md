# GraphSpec 规范

> 本仓库 **Session Evolution Graph**（`session-evolution-graph`）的教学示例对齐此规范。

## 简介

GraphSpec 是 GraphForge 问题演化图谱的数据规范，定义：

- **实体类型**：Research、Problem、Version、Report、Artifact
- **关系类型**：Research→Problem、Problem→Problem（derived）、Problem→Report
- **阶段**：explore → design → implement → completed

## 数据文件

- `evolution.json` — 研究演化链
- `timeline_events.json` — 时间线事件
- `topics_data.json` — 主题详情

## 规模

- 10 个技术主题
- 256 个问题节点
- 30 个版本阶段
- 63 条演化三元组

（完整规范见 GraphForge 项目）
