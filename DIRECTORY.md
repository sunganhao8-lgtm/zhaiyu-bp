# 宅域项目 — 实际目录树

> 来自 `data/structure.yaml` 的注解 + 真实文件系统
> 自动生成于：执行 `python tools/render_directory.py --write`
> 生成时间：2026-06-27 11:24

```
zhaiyu-bp/  ← 宅域宠物洗护店项目 — 知识库根目录
├── archive/
│   └── 2026-06-16/
│       ├── inputs/
│       │   ├── refs/
│       │   │   └── ... (省略深层文件)
│       │   └── INDEX.md
│       ├── outputs/
│       │   ├── candidates/
│       │   └── INDEX.md
│       ├── review/
│       │   ├── archive/
│       │   └── INDEX.md
│       ├── work/
│       │   ├── frames/
│       │   │   └── ... (省略深层文件)
│       │   ├── INDEX.md
│       │   ├── floor-plan-crop.png
│       │   ├── floor-plan-only.png
│       │   ├── layout-final-preview.png
│       │   ├── layout-preview-v2.png
│       │   ├── layout-preview.png
│       │   └── layout-v1.html
│       ├── DJI_20260616202147_0003_D.MP4
│       ├── 宅电logo截图.png
│       └── 宅电logo设计.png
├── assets/
│   └── zhaiyu-logo.png
├── bps/
│   ├── landing-for-coop/
│   │   ├── .github/
│   │   │   └── workflows/
│   │   │       └── ... (省略深层文件)
│   │   ├── assets/
│   │   │   ├── bp-1-zhaiyu.jpeg
│   │   │   ├── bp-2-funding.jpeg
│   │   │   ├── bp-3-slide.jpeg
│   │   │   └── qrcode-placeholder.png
│   │   ├── README.md
│   │   ├── hermes-feishu-notifier-path.md
│   │   ├── hermes-optimization-5.md
│   │   ├── index.html
│   │   └── landing.html
│   └── store-front/
│       ├── .github/
│       │   ├── ISSUE_TEMPLATE/
│       │   │   └── ... (省略深层文件)
│       │   └── workflows/
│       │       └── ... (省略深层文件)
│       ├── assets/
│       │   ├── review-1-zhaiyu.png
│       │   ├── review-2-doc.png
│       │   ├── review-layout-v6.9.29-final.jpeg
│       │   ├── review-layout-v6.9.29.jpeg
│       │   ├── review-mobile-zhaiyu.png
│       │   ├── review-mobile-zhaiyu2.png
│       │   ├── review-mobile-zhaiyu3.png
│       │   ├── review-mobile-zhaiyu4.png
│       │   └── ... +12 more files
│       ├── data/
│       │   └── poi.json
│       ├── landing-assets/
│       │   ├── bp-1-zhaiyu.jpeg
│       │   ├── bp-2-funding.jpeg
│       │   └── bp-3-slide.jpeg
│       ├── .gitignore
│       ├── CHANGELOG.md
│       ├── CONTRIBUTING.md
│       ├── DECISIONS.md
│       ├── INDEX.md
│       ├── LICENSE
│       ├── PARTNER_FAQ.md
│       ├── PROJECT_HISTORY.md
│       └── ... +11 more files
├── data/
│   ├── decisions.yaml
│   ├── facts.yaml
│   └── structure.yaml
├── docs/
│   └── structure.md
├── meetings/
│   ├── 2026-06-26-孙淦浩快速会议.md
│   └── _template.md
├── raw/
│   └── meetings/
│       └── 2026-06-26/
│           ├── README.md
│           ├── 孙淦浩的快速会议-AI纪要.txt
│           └── 开店成本收益分析.xlsx
├── tools/
│   ├── render_directory.py
│   ├── render_index.py
│   ├── render_structure.py
│   └── verify.py
├── .gitignore
├── DECISIONS.md
├── DIRECTORY.md
├── INDEX.md
└── README.md
```

## 🏷️ 受众标签

- **ai** — 主要给 AI 读（结构化数据、规则）
- **human** — 主要给人读（笔记、说明）
- **partner** — 给合伙人/外人看（演示、报告）
- **self** — 自己用，不分享

## 🎯 关键路径速查

| 我想 | 去这里 |
|---|---|
| 改任何数字 | `data/facts.yaml` |
| 加新决议 | `data/decisions.yaml` + `meetings/YYYY-MM-DD-*.md` |
| 改 BP 给投资人看 | `bps/store-front/bp.html` |
| 查会议说过什么 | `meetings/` 目录 |
| 看原始纪要/录屏 | `raw/meetings/` 目录 |
| 改完跑校验 | `python tools/verify.py` |
| 重出本图 | `python tools/render_directory.py --write` |