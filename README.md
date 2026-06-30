# 宅域 (Zhaiyu) — 宠物洗护 + 电竞样板间 · 创业项目

> **宠物现金流 · 电竞样板间 · 自媒体矩阵**
> 12 万启动 · 月固定 9850 元 · 日目标营收 750 元 · 12 个月回本目标

---

## 这是什么

宅域（zhaiyu）是一个位于**临港泥城**的社区门店创业项目。首期以**宠物洗护/美容/寄养**承担稳定现金流，同时在干区设置**电竞房样板间**，用于合伙人工作、内容拍摄、桌搭好物展示和上门电竞房搭建服务转化。

这个仓库是项目的**知识库**——包括商业计划书、会议记录、财务模型、合作着陆页、执行方案、以及保证文档一致性的工具。

## 怎么用

| 你想做的事 | 入口 |
|---|---|
| 快速了解项目全貌 | [[INDEX.md]] |
| 看所有关键决策 | [[DECISIONS.md]]（或 [[data/decisions.yaml]] 结构化版） |
| 读最新会议笔记 | [[meetings/2026-06-26-创始人A快速会议.md]] |
| 看商业计划书（网页版） | [[bps/store-front/bp.html]] |
| 看商业计划书（Markdown 源） | [[bps/store-front/bp.md]] |
| 看合作着陆页 | [[bps/landing-for-coop/landing.html]] |
| 看优化后的执行方案 | [[docs/optimization-plan.md]] |
| 查事实/数字（唯一数据源） | [[data/facts.yaml]] |
| 校验数字一致性 | `python tools/verify.py` |

## 项目结构

```
zhaiyu-bp/
├── data/              ← 📊 事实与决策数据源（YAML，唯一来源）
├── meetings/          ← 📝 会议笔记（含冲突追踪）
├── bps/               ← 📦 业务交付物
│   ├── store-front/   ←   门店商业计划书（bp.html/bp.md）
│   └── landing-for-coop/  ←   合作着陆页
├── raw/               ← 📄 原始素材原样归档（纪要/Excel/录屏）
├── tools/             ← 🔧 一致性工具（verify.py / render_index.py）
├── assets/            ← 🖼️ 共享资源（Logo 等）
└── archive/           ← 🗄️ 旧版工作文件归档
```

## 为什么这样设计

这个项目的知识库记录了从立项到现在的所有**决策轨迹**，目的是解决两个常见问题：

1. **改文档漏改** — 修改 A 文件时 B 文件忘记同步。`data/facts.yaml` 是唯一事实源，`tools/verify.py` 可自动扫描不一致。
2. **新旧会议冲突** — 新会议的决定和之前定好的事项冲突。每篇会议笔记的「冲突追踪」段（第 3 段）**强制**记录与哪些历史决议冲突。
3. **业务发散** — 宠物、电竞、饮品、活动、AI 培训等想法必须分层管理：首期必做 / 样板展示 / 验证后做 / 暂不做或需资质。

## 快速开始

```bash
# 检查一致性（修改 BP 后必跑）
python tools/verify.py

# 更新 INDEX
python tools/render_index.py --write
```

---

> 关于这个项目的完整故事：[[PROJECT_HISTORY.md]]（在 bps/store-front/ 下）
