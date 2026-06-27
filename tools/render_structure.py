#!/usr/bin/env python3
"""
宅域目录结构 — Mermaid 可视化生成器 (render_structure.py)
============================================================
读取 data/structure.yaml，输出 docs/structure.md：
- Mermaid 框图（视觉直观）
- 表格版（方便搜索/复制）

用法：
    python tools/render_structure.py          # 输出到终端
    python tools/render_structure.py --write  # 写入 docs/structure.md
"""

import os
import sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRUCT_PATH = os.path.join(ROOT, "data", "structure.yaml")
OUTPUT_PATH = os.path.join(ROOT, "docs", "structure.md")


def load_structure():
    with open(STRUCT_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def flatten(structure):
    """把嵌套结构扁平化为 (path, info) 列表"""
    items = []
    root_info = {k: v for k, v in structure["root"].items() if k != "contains"}
    root_info["path"] = "zhaiyu-bp/"
    root_info["type"] = "dir"
    items.append(root_info)

    def recurse(node, parent_path=""):
        for child in node.get("contains", []):
            child_path = child["path"]
            # 现在所有子项已经是相对父目录的路径（不含 zhaiyu-bp/）
            if parent_path:
                full_path = parent_path.rstrip("/") + "/" + child_path
            else:
                # 根级子项，路径以 zhaiyu-bp/ 开头
                full_path = "zhaiyu-bp/" + child_path
            full_path = full_path.replace("\\", "/")
            info = {k: v for k, v in child.items() if k != "contains"}
            info["path"] = full_path
            items.append(info)
            if child.get("type") == "dir":
                recurse(child, full_path)

    recurse(structure["root"])
    return items


def build_mermaid(items):
    """生成 Mermaid 框图"""
    lines = ["```mermaid", "graph TD"]
    lines.append("    classDef rootStyle fill:#7B2CBF,stroke:#5A189A,color:#fff,stroke-width:3px;")
    lines.append("    classDef dataStyle fill:#3A86FF,stroke:#2667CC,color:#fff;")
    lines.append("    classDef meetStyle fill:#FB5607,stroke:#C2410C,color:#fff;")
    lines.append("    classDef bpStyle fill:#06A77D,stroke:#048A66,color:#fff;")
    lines.append("    classDef rawStyle fill:#9D4EDD,stroke:#7B2CBF,color:#fff;")
    lines.append("    classDef toolStyle fill:#FFB703,stroke:#FB8500,color:#000;")
    lines.append("    classDef docStyle fill:#EF476F,stroke:#C0306B,color:#fff;")
    lines.append("    classDef archStyle fill:#6B7280,stroke:#4B5563,color:#fff;")
    lines.append("")

    # 节点 ID
    def node_id(path):
        return "n" + str(abs(hash(path)) % 100000)

    # 生成节点
    id_map = {}
    for item in items:
        path = item["path"]
        if path == "zhaiyu-bp/":
            nid = "ROOT"
        else:
            nid = node_id(path)
        id_map[path] = nid

        # 简化显示名（去掉 zhaiyu-bp/ 前缀）
        name = path
        if name.startswith("zhaiyu-bp/"):
            name = name[len("zhaiyu-bp/"):]
        if not name:
            name = "zhaiyu-bp/"

        # 节点标签（用 <br/> 换行，HTML实体编码）
        purpose = item.get("purpose", "").split("—")[0].strip()[:35]
        purpose_clean = purpose.replace('"', "'")
        label = f"<b>{name}</b><br/>{purpose_clean}" if purpose_clean else f"<b>{name}</b>"
        # Mermaid 在 markdown 里能渲染 HTML 标签
        lines.append(f'    {nid}["{label}"]')

    lines.append("")

    # 生成边
    for item in items:
        path = item["path"]
        if path == "zhaiyu-bp/":
            continue
        # 找父路径
        parts = path.rsplit("/", 1)
        parent_path = parts[0] if len(parts) > 1 else "zhaiyu-bp/"
        if parent_path not in id_map:
            parent_path = "zhaiyu-bp/"
        lines.append(f"    {id_map[parent_path]} --> {id_map[path]}")

    # 应用样式
    for item in items:
        path = item["path"]
        nid = id_map[path]
        if path == "zhaiyu-bp/":
            lines.append(f"    class ROOT rootStyle;")
            continue
        if path.startswith("data/") or "facts.yaml" in path or "decisions.yaml" in path or "structure.yaml" in path:
            lines.append(f"    class {nid} dataStyle;")
        elif path.startswith("meetings/") or "会议笔记" in path:
            lines.append(f"    class {nid} meetStyle;")
        elif path.startswith("bps/"):
            lines.append(f"    class {nid} bpStyle;")
        elif path.startswith("raw/"):
            lines.append(f"    class {nid} rawStyle;")
        elif path.startswith("tools/"):
            lines.append(f"    class {nid} toolStyle;")
        elif path.startswith("archive/") or ".git/" in path:
            lines.append(f"    class {nid} archStyle;")
        elif path.endswith(".md") or path == "README.md" or path == "INDEX.md" or path == "DECISIONS.md" or path == "DIRECTORY.md":
            lines.append(f"    class {nid} docStyle;")

    lines.append("```")
    return "\n".join(lines)


def build_table(items):
    """生成 Markdown 表格"""
    lines = ["| 路径 | 类型 | 用途 | 受众 | 何时读 | 何时写 |", "|---|---|---|---|---|---|"]
    for item in items:
        if item["path"] == "zhaiyu-bp/":
            continue
        path = f"`{item['path']}`"
        type_str = "📁 目录" if item["type"] == "dir" else "📄 文件"
        purpose = item.get("purpose", "—").replace("|", "/").replace("\n", " ")[:60]
        audience = ",".join(item.get("audience", []))
        read_when = item.get("read_when", "—").replace("|", "/")[:40]
        write_when = item.get("write_when", "—").replace("|", "/")[:40]
        lines.append(f"| {path} | {type_str} | {purpose} | {audience} | {read_when} | {write_when} |")
    return "\n".join(lines)


def build_workflow():
    """生成工作流说明"""
    return """
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
"""


def build_color_legend():
    return """
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
"""


def main():
    structure = load_structure()
    items = flatten(structure)

    output = []
    output.append("# 宅域知识库 — 目录结构图\n")
    output.append("> 自动生成于 `data/structure.yaml`")
    output.append("> 改结构后跑 `python tools/render_structure.py --write` 重新生成")
    output.append(f"> 当前共 {len(items)} 个节点\n")
    output.append("---\n")

    output.append("## 📊 Mermaid 可视化\n")
    output.append(build_mermaid(items))
    output.append("\n---\n")

    output.append("## 📋 完整目录表\n")
    output.append(build_table(items))
    output.append("\n---\n")

    output.append(build_color_legend())
    output.append(build_workflow())

    content = "\n".join(output)

    if "--write" in sys.argv:
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已写入 {OUTPUT_PATH}")
    else:
        print(content)


if __name__ == "__main__":
    main()
