# 宅域知识库 — 目录结构图

> 自动生成于 `data/structure.yaml`
> 改结构后跑 `python tools/render_structure.py --write` 重新生成
> 当前共 37 个节点

---

## 📊 Mermaid 可视化

```mermaid
graph TD
    classDef rootStyle fill:#7B2CBF,stroke:#5A189A,color:#fff,stroke-width:3px;
    classDef dataStyle fill:#3A86FF,stroke:#2667CC,color:#fff;
    classDef meetStyle fill:#FB5607,stroke:#C2410C,color:#fff;
    classDef bpStyle fill:#06A77D,stroke:#048A66,color:#fff;
    classDef rawStyle fill:#9D4EDD,stroke:#7B2CBF,color:#fff;
    classDef toolStyle fill:#FFB703,stroke:#FB8500,color:#000;
    classDef docStyle fill:#EF476F,stroke:#C0306B,color:#fff;
    classDef archStyle fill:#6B7280,stroke:#4B5563,color:#fff;

    ROOT["&lt;b&gt;zhaiyu-bp/&lt;/b&gt;&lt;br/&gt;宅域宠物洗护店项目"]
    n59258["&lt;b&gt;data/&lt;/b&gt;&lt;br/&gt;唯一事实源"]
    n70084["&lt;b&gt;data/data/facts.yaml&lt;/b&gt;&lt;br/&gt;启动资金/成本/股份/服务定价等所有数字"]
    n84194["&lt;b&gt;data/data/decisions.yaml&lt;/b&gt;&lt;br/&gt;17 条决策记录（含历史、已替换、生效）"]
    n47108["&lt;b&gt;meetings/&lt;/b&gt;&lt;br/&gt;会议笔记"]
    n46223["&lt;b&gt;meetings/meetings/_template.md&lt;/b&gt;&lt;br/&gt;四段式会议笔记模板（强制冲突追踪）"]
    n69962["&lt;b&gt;meetings/meetings/2026-06-26-孙淦浩快速会议.md&lt;/b&gt;&lt;br/&gt;第一次正式会议（启动资金/股份/分润机制敲定）"]
    n63719["&lt;b&gt;bps/&lt;/b&gt;&lt;br/&gt;业务交付物"]
    n36944["&lt;b&gt;bps/bps/store-front/&lt;/b&gt;&lt;br/&gt;门店商业计划书（bp.html/bp.md/布局编辑器/选址"]
    n82056["&lt;b&gt;bps/bps/landing-coop/&lt;/b&gt;&lt;br/&gt;合作着陆页（小红书引流/招合伙人）"]
    n53752["&lt;b&gt;bps/bps/store-front/bp.html&lt;/b&gt;&lt;br/&gt;商业计划书网页版（18页幻灯片）"]
    n21710["&lt;b&gt;bps/bps/store-front/bp.md&lt;/b&gt;&lt;br/&gt;商业计划书 Markdown 源文档（含财务明细）"]
    n63212["&lt;b&gt;bps/bps/store-front/site-map.html&lt;/b&gt;&lt;br/&gt;选址分析地图（高德API + 11个真实POI）"]
    n27861["&lt;b&gt;bps/bps/store-front/layout-editor.html&lt;/b&gt;&lt;br/&gt;49㎡ 门店布局编辑器（Konva.js + 碰撞检测）"]
    n82957["&lt;b&gt;bps/bps/landing-coop/landing.html&lt;/b&gt;&lt;br/&gt;合作着陆页主入口"]
    n95372["&lt;b&gt;bps/bps/landing-coop/index.html&lt;/b&gt;&lt;br/&gt;合作着陆页重定向页"]
    n15598["&lt;b&gt;raw/&lt;/b&gt;&lt;br/&gt;原始素材"]
    n51937["&lt;b&gt;raw/raw/meetings/2026-06-26/&lt;/b&gt;&lt;br/&gt;2026-06-26 会议的原始素材"]
    n29294["&lt;b&gt;raw/raw/meetings/2026-06-26/元宝纪要.txt&lt;/b&gt;&lt;br/&gt;元宝AI纪要全量文字（73KB）"]
    n15846["&lt;b&gt;raw/raw/meetings/2026-06-26/成本收益分析.xlsx&lt;/b&gt;&lt;br/&gt;会议填写的财务模型"]
    n7676["&lt;b&gt;raw/raw/meetings/2026-06-26/README.md&lt;/b&gt;&lt;br/&gt;该素材包的说明 + 录屏位置指引"]
    n10072["&lt;b&gt;tools/&lt;/b&gt;&lt;br/&gt;一致性工具"]
    n47912["&lt;b&gt;tools/tools/verify.py&lt;/b&gt;&lt;br/&gt;一致性校验（扫旧数字残留/不存在的DEC引用/未同步决议）"]
    n18138["&lt;b&gt;tools/tools/render_index.py&lt;/b&gt;&lt;br/&gt;自动生成 INDEX.md"]
    n74296["&lt;b&gt;tools/tools/render_structure.py&lt;/b&gt;&lt;br/&gt;自动生成 docs/structure.md（Mermaid"]
    n60295["&lt;b&gt;tools/tools/render_directory.py&lt;/b&gt;&lt;br/&gt;自动生成 DIRECTORY.md（实景目录树+说明）"]
    n94508["&lt;b&gt;assets/&lt;/b&gt;&lt;br/&gt;共享资源（Logo、品牌素材）"]
    n74167["&lt;b&gt;assets/assets/zhaiyu-logo.png&lt;/b&gt;&lt;br/&gt;宅域品牌 Logo"]
    n23682["&lt;b&gt;archive/&lt;/b&gt;&lt;br/&gt;旧版本/工作过程文件归档"]
    n62251["&lt;b&gt;archive/archive/2026-06-16/&lt;/b&gt;&lt;br/&gt;立项当天的工作文件（inputs/outputs/revie"]
    n11518["&lt;b&gt;README.md&lt;/b&gt;&lt;br/&gt;项目入口（'这是什么/怎么用/为什么这样设计'）"]
    n51985["&lt;b&gt;INDEX.md&lt;/b&gt;&lt;br/&gt;自动生成的知识地图（不要手改）"]
    n90051["&lt;b&gt;DECISIONS.md&lt;/b&gt;&lt;br/&gt;决策记录人类可读版（数据源在 data/decisions."]
    n24579["&lt;b&gt;DIRECTORY.md&lt;/b&gt;&lt;br/&gt;目录结构总览（自动生成，给合伙人看的）"]
    n41900["&lt;b&gt;docs/structure.md&lt;/b&gt;&lt;br/&gt;目录结构 Mermaid 可视化图（自动生成）"]
    n33364["&lt;b&gt;.gitignore&lt;/b&gt;&lt;br/&gt;忽略规则（大文件/中间产物不入库）"]
    n52895["&lt;b&gt;.git/&lt;/b&gt;&lt;br/&gt;Git 仓库元数据"]

    ROOT --> n59258
    ROOT --> n70084
    ROOT --> n84194
    ROOT --> n47108
    ROOT --> n46223
    ROOT --> n69962
    ROOT --> n63719
    ROOT --> n36944
    ROOT --> n82056
    ROOT --> n53752
    ROOT --> n21710
    ROOT --> n63212
    ROOT --> n27861
    ROOT --> n82957
    ROOT --> n95372
    ROOT --> n15598
    ROOT --> n51937
    ROOT --> n29294
    ROOT --> n15846
    ROOT --> n7676
    ROOT --> n10072
    ROOT --> n47912
    ROOT --> n18138
    ROOT --> n74296
    ROOT --> n60295
    ROOT --> n94508
    ROOT --> n74167
    ROOT --> n23682
    ROOT --> n62251
    ROOT --> n11518
    ROOT --> n51985
    ROOT --> n90051
    ROOT --> n24579
    ROOT --> n41900
    ROOT --> n33364
    ROOT --> n52895
    class ROOT rootStyle;
    class n59258 dataStyle;
    class n70084 dataStyle;
    class n84194 dataStyle;
    class n47108 meetStyle;
    class n46223 meetStyle;
    class n69962 meetStyle;
    class n63719 bpStyle;
    class n36944 bpStyle;
    class n82056 bpStyle;
    class n53752 bpStyle;
    class n21710 bpStyle;
    class n63212 bpStyle;
    class n27861 bpStyle;
    class n82957 bpStyle;
    class n95372 bpStyle;
    class n15598 rawStyle;
    class n51937 rawStyle;
    class n29294 rawStyle;
    class n15846 rawStyle;
    class n7676 rawStyle;
    class n10072 toolStyle;
    class n47912 toolStyle;
    class n18138 toolStyle;
    class n74296 toolStyle;
    class n60295 toolStyle;
    class n23682 archStyle;
    class n62251 archStyle;
    class n11518 docStyle;
    class n51985 docStyle;
    class n90051 docStyle;
    class n24579 docStyle;
    class n41900 docStyle;
    class n52895 archStyle;
```

---

## 📋 完整目录表

| 路径 | 类型 | 用途 | 受众 | 何时读 | 何时写 |
|---|---|---|---|---|---|
| `data/` | 📁 目录 | 唯一事实源 — 所有数字/决策的结构化存储 | ai | 需要确认某个数字、查找某条决策 | 任何数字/决议变化（**必须第一个改这里**） |
| `data/data/facts.yaml` | 📄 文件 | 启动资金/成本/股份/服务定价等所有数字 | ai | AI 回答任何财务/数字问题前 | 财务模型调整 |
| `data/data/decisions.yaml` | 📄 文件 | 17 条决策记录（含历史、已替换、生效） | ai | 解释"为什么这样设计" / 追溯决策时间线 | 任何新决议、修订、废弃 |
| `meetings/` | 📁 目录 | 会议笔记 — 每次会议的"决议+冲突+待办"结构化记录 | ai,human,partner | 了解一次会议的决定 / 找历史讨论 | 每次会议后立刻写一篇 |
| `meetings/meetings/_template.md` | 📄 文件 | 四段式会议笔记模板（强制冲突追踪） | human | — | — |
| `meetings/meetings/2026-06-26-孙淦浩快速会议.md` | 📄 文件 | 第一次正式会议（启动资金/股份/分润机制敲定） | ai,human,partner | — | — |
| `bps/` | 📁 目录 | 业务交付物 — 给外人看的成品 | partner,investor,customer | 给投资人/合伙人/客户演示 | 演示材料更新 |
| `bps/bps/store-front/` | 📁 目录 | 门店商业计划书（bp.html/bp.md/布局编辑器/选址地图） |  | — | — |
| `bps/bps/landing-coop/` | 📁 目录 | 合作着陆页（小红书引流/招合伙人） |  | — | — |
| `bps/bps/store-front/bp.html` | 📄 文件 | 商业计划书网页版（18页幻灯片） | partner,investor | — | — |
| `bps/bps/store-front/bp.md` | 📄 文件 | 商业计划书 Markdown 源文档（含财务明细） | partner | — | — |
| `bps/bps/store-front/site-map.html` | 📄 文件 | 选址分析地图（高德API + 11个真实POI） |  | — | — |
| `bps/bps/store-front/layout-editor.html` | 📄 文件 | 49㎡ 门店布局编辑器（Konva.js + 碰撞检测） |  | — | — |
| `bps/bps/landing-coop/landing.html` | 📄 文件 | 合作着陆页主入口 |  | — | — |
| `bps/bps/landing-coop/index.html` | 📄 文件 | 合作着陆页重定向页 |  | — | — |
| `raw/` | 📁 目录 | 原始素材 — 元宝纪要/Excel/录屏，按"原样"归档 | human | 查证某个数字/引述/录屏内容 | 每次新会议/新素材 |
| `raw/raw/meetings/2026-06-26/` | 📁 目录 | 2026-06-26 会议的原始素材 |  | — | — |
| `raw/raw/meetings/2026-06-26/元宝纪要.txt` | 📄 文件 | 元宝AI纪要全量文字（73KB） |  | — | — |
| `raw/raw/meetings/2026-06-26/成本收益分析.xlsx` | 📄 文件 | 会议填写的财务模型 |  | — | — |
| `raw/raw/meetings/2026-06-26/README.md` | 📄 文件 | 该素材包的说明 + 录屏位置指引 |  | — | — |
| `tools/` | 📁 目录 | 一致性工具 — 保证知识库不自相矛盾 | ai | 改完任何文件后 | 新规则/新校验 |
| `tools/tools/verify.py` | 📄 文件 | 一致性校验（扫旧数字残留/不存在的DEC引用/未同步决议） |  | — | — |
| `tools/tools/render_index.py` | 📄 文件 | 自动生成 INDEX.md |  | — | — |
| `tools/tools/render_structure.py` | 📄 文件 | 自动生成 docs/structure.md（Mermaid图+表格） |  | — | — |
| `tools/tools/render_directory.py` | 📄 文件 | 自动生成 DIRECTORY.md（实景目录树+说明） |  | — | — |
| `assets/` | 📁 目录 | 共享资源（Logo、品牌素材） | human | — | — |
| `assets/assets/zhaiyu-logo.png` | 📄 文件 | 宅域品牌 Logo |  | — | — |
| `archive/` | 📁 目录 | 旧版本/工作过程文件归档 | human | 想看"当时怎么做的" | 任何旧文件需要归档时 |
| `archive/archive/2026-06-16/` | 📁 目录 | 立项当天的工作文件（inputs/outputs/review/work） |  | — | — |
| `README.md` | 📄 文件 | 项目入口（"这是什么/怎么用/为什么这样设计"） | human,partner | 第一次打开项目 | 入口/导航逻辑变化 |
| `INDEX.md` | 📄 文件 | 自动生成的知识地图（不要手改） | ai,human | — | — |
| `DECISIONS.md` | 📄 文件 | 决策记录人类可读版（数据源在 data/decisions.yaml） | ai,human,partner | 了解项目所有关键决策 | — |
| `DIRECTORY.md` | 📄 文件 | 目录结构总览（自动生成，给合伙人看的） | human,partner | — | — |
| `docs/structure.md` | 📄 文件 | 目录结构 Mermaid 可视化图（自动生成） | human,partner | — | — |
| `.gitignore` | 📄 文件 | 忽略规则（大文件/中间产物不入库） |  | — | — |
| `.git/` | 📁 目录 | Git 仓库元数据 |  | — | — |

---


## 🎨 颜色说明

| 颜色 | 含义 | 例子 |
|---|---|---|
| 🟣 紫色 (root) | 项目根 | zhaiyu-bp/ |
| 🔵 蓝色 (data) | 数据源（机器读的真相） | data/facts.yaml |
| 🟠 橙色 (meetings) | 会议笔记 | meetings/2026-06-26-...md |
| 🟢 绿色 (bps) | 业务交付物（给外人看的） | bps/store-front/bp.html |
| 🟪 浅紫 (raw) | 原始素材（人类查证用） | raw/meetings/2026-06-26/ |
| 🟡 黄色 (tools) | 工具脚本 | tools/verify.py |
| 🔴 红色 (docs) | 文档入口 | README.md / DECISIONS.md |
| ⚫ 灰色 (archive) | 归档 | archive/2026-06-16/ |


## 🔄 标准工作流

### 场景 1：改一个数字（比如启动资金 12万 → 15万）

```bash
# 1. 先改唯一数据源
# 编辑 data/facts.yaml 的 startup.total

# 2. 同步到所有引用此数字的文档
# 编辑 bps/store-front/bp.html / bp.md
# 编辑 bps/store-front/README.md
# 编辑 DECISIONS.md

# 3. 跑校验
python tools/verify.py
# 必须输出: ✅ 通过！

# 4. 提交
git add . && git commit -m "调整启动资金 12→15万"
```

### 场景 2：开了一次新会议

```bash
# 1. 把素材丢到 raw/
cp 元宝纪要.txt raw/meetings/2026-07-15/
cp 会议.xlsx raw/meetings/2026-07-15/

# 2. 复制模板写笔记
cp meetings/_template.md meetings/2026-07-15-xxx.md
# 必须填第3段（冲突追踪）！没有就写"无冲突"

# 3. 加 DEC 条目
# 编辑 data/decisions.yaml
# 编辑 meetings/2026-07-15-xxx.md 的第2段

# 4. 跑校验
python tools/verify.py
python tools/render_index.py --write
```

### 场景 3：调整目录结构

```bash
# 1. 编辑 data/structure.yaml（这是结构的事实源）
# 2. 跑这个脚本重出图
python tools/render_structure.py --write
python tools/render_directory.py --write
# 3. 实际移动文件
# 4. 跑校验
python tools/verify.py
```
