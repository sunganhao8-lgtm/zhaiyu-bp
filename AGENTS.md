# AGENTS.md — 宅域知识库工作指南

宅域（zhaiyu-bp）是临港泥城社区门店创业项目的**知识库仓库**：商业计划书、会议记录、财务口径、决策记录（ADR）、合作着陆页及一致性校验工具。仓库语言为中文。

## 目录速查

| 目录/文件 | 作用 |
|---|---|
| `data/facts.yaml` | **唯一数据源**：所有数字/事实以此为准 |
| `data/decisions.yaml` | 决策记录（ADR）结构化源头，DEC-NNN 编号 |
| `DECISIONS.md` / `INDEX.md` / `DIRECTORY.md` | 自动/半自动生成的快照，不要手改（见下方命令） |
| `bp.html`（根目录） | 投资人版商业计划书（当前生效版本） |
| `meetings/` | 会议笔记，必须按 `_template.md` 四段结构写 |
| `bps/` | 交付物：`store-front/`（BP 镜像）、`landing-for-coop/`（着陆页） |
| `src/light-home.js` | Three.js 互动首页源码（three@0.185.1 + three-html-render） |
| `tools/` | `verify.py` / `render_index.py` / `render_directory.py` 等 |
| `raw/`、`archive/`、`tmp/`、`.tmp/` | 原始素材与归档，只读，不做一致性扫描 |
| `产品图/`、`装修/`、`assets/` | 图片素材（中文目录名，仅本地用） |

## 常用命令

```bash
npm install && npm run build   # esbuild 打包 src/light-home.js → assets/light-home.js
npm run check                  # 语法检查（CI 会跑）
python tools/verify.py         # 一致性校验（改任何数字/BP 后必跑；退出码 0=OK 1=警告 2=错误）
python tools/render_index.py --write        # 重新生成 INDEX.md
python tools/render_directory.py --write    # 重新生成 DIRECTORY.md
python -m http.server 8765     # 本地预览（首页 index.html，完整 BP 为 bp.html）
```

## 硬性规则（违反会导致 verify.py 报错或文档失一致）

1. **改数字三处同步**：`data/facts.yaml` → `bp.html`（verify.py 用 `BP_REQUIRED_SNIPPETS` 检查固定文案片段）→ `tools/verify.py` 顶部的 `EXPECTED` 字典（启动资金 182300、月固定 6416、租金 3233、面积 59.87㎡ 等全部硬编码）。只改一处必挂校验。
2. **加决策**：写入 `data/decisions.yaml`（唯一 ID `DEC-NNN`），同时在对应会议笔记中引用。被取代的决策**不删除**，标 `status: superseded` + `superseded_by: DEC-XXX`（如 DEC-031→DEC-032）。
3. **会议笔记**：按 `meetings/_template.md` 四段结构；第 3 段「与历史决议的冲突」**强制填写**，无冲突也要显式写"无冲突"。
4. **新业务分层**：不能凭空加业务想法；首期必做 / 样板展示 / 验证后做 / 暂不做四层，新业务须来自客户发言档案的重复需求。

## 部署与平台坑

- GitHub Pages：push 到 `main` 即触发 `.github/workflows/pages.yml`（Node 24 构建 light-home.js 后整仓部署，`.nojekyll` 已配置）。
- **中文路径在 GitHub Pages 100% 404**：所有会被 Pages 引用的文件必须用英文文件名（曾因 `产品图/...` 中文路径全 404，改为 `assets/devices/...` 修复，见 commit d653470）。中文目录名仅限本地素材目录。
- 本机为 Windows + Git Bash，仓库内已有中文文件名，shell 命令处理中文路径时注意引号。

## 改动前先读

- 动数字/财务口径前：`data/facts.yaml` 头部注释 + `README.md` 的「为什么这样设计」。
- 动 BP 前确认口径版本：当前生效 = 启动资金 18.23 万（DEC-032 无转让费口径）、月固定 6416 元（DEC-029）、主体架构个体户先行 + 个转企（DEC-036）。
- 投资人问答口径见 `docs/investor-objection-playbook.md`（DEC-028）。
