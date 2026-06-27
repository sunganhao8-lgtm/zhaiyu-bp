#!/usr/bin/env python3
"""
宅域目录结构 — 实景目录树生成器 (render_directory.py)
====================================================
扫描真实文件系统 + data/structure.yaml，输出 DIRECTORY.md：
- 真实目录树（带注释）
- 给合伙人快速看"我们的项目结构长啥样"

用法：
    python tools/render_directory.py
    python tools/render_directory.py --write
"""

import os
import sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRUCT_PATH = os.path.join(ROOT, "data", "structure.yaml")
OUTPUT_PATH = os.path.join(ROOT, "DIRECTORY.md")

SKIP = {".git", "__pycache__", "node_modules", "vendor"}
SKIP_EXTS = {".wemtv", ".wemta", ".wemtc", ".wemtvidx", ".wemtaidx"}


def load_purposes():
    """从 structure.yaml 加载所有路径的说明"""
    with open(STRUCT_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    purposes = {}
    audiences = {}

def walk(node, parent=""):
    for child in node.get("contains", []):
        child_path = child["path"]
        # 已经是绝对路径了（以 zhaiyu-bp/ 开头）
        if child_path.startswith("zhaiyu-bp/"):
            full = child_path
        else:
            full = os.path.join(parent, child_path) if parent else child_path
        full = full.replace("\\", "/")
        if "purpose" in child:
            purposes[full] = child["purpose"]
        if "audience" in child:
            audiences[full] = child["audience"]
        if child.get("type") == "dir":
            walk(child, full)

    walk(data["root"])
    purposes["zhaiyu-bp/"] = data["root"].get("purpose", "")
    audiences["zhaiyu-bp/"] = data["root"].get("audience", [])
    return purposes, audiences


def build_tree(path, purposes, audiences, prefix="", max_depth=4, current_depth=0):
    """生成带注释的目录树（限制深度）"""
    if current_depth >= max_depth:
        return [f"{prefix}└── ... (省略深层文件)"] if os.listdir(path) else []
    
    lines = []
    items = sorted(os.listdir(path))
    items = [i for i in items if i not in SKIP and not any(i.endswith(e) for e in SKIP_EXTS)]

    dirs = [i for i in items if os.path.isdir(os.path.join(path, i))]
    files = [i for i in items if os.path.isfile(os.path.join(path, i))]

    # 文件超过10个时折叠
    if len(files) > 10:
        files = files[:8] + [f"... +{len(files)-8} more files"]

    all_items = [(d, True) for d in dirs] + [(f, False) for f in files]

    for idx, (name, is_dir) in enumerate(all_items):
        is_last = (idx == len(all_items) - 1)
        connector = "└── " if is_last else "├── "
        child_prefix = "    " if is_last else "│   "

        full_path = os.path.relpath(os.path.join(path, name), ROOT).replace("\\", "/")
        rel = full_path + "/" if is_dir else full_path

        purpose = purposes.get(rel, purposes.get(full_path, ""))
        aud = audiences.get(rel, audiences.get(full_path, []))
        aud_str = f" [{','.join(aud)}]" if aud and aud != ["ai"] else ""

        display = f"{name}{'/' if is_dir else ''}"
        annotation = f"  ← {purpose}{aud_str}" if purpose and is_dir else ""
        lines.append(f"{prefix}{connector}{display}{annotation}")

        if is_dir:
            sub_path = os.path.join(path, name)
            lines.extend(build_tree(sub_path, purposes, audiences, 
                                   prefix + child_prefix, max_depth, current_depth + 1))

    return lines


def main():
    purposes, audiences = load_purposes()

    lines = []
    lines.append("# 宅域项目 — 实际目录树\n")
    lines.append("> 来自 `data/structure.yaml` 的注解 + 真实文件系统")
    lines.append("> 自动生成于：执行 `python tools/render_directory.py --write`")
    from datetime import datetime
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("```")
    lines.append("zhaiyu-bp/  ← " + purposes.get("zhaiyu-bp/", "项目根目录"))
    lines.extend(build_tree(ROOT, purposes, audiences))
    lines.append("```")

    # 分类说明
    lines.append("")
    lines.append("## 🏷️ 受众标签\n")
    lines.append("- **ai** — 主要给 AI 读（结构化数据、规则）")
    lines.append("- **human** — 主要给人读（笔记、说明）")
    lines.append("- **partner** — 给合伙人/外人看（演示、报告）")
    lines.append("- **self** — 自己用，不分享")
    lines.append("")

    lines.append("## 🎯 关键路径速查\n")
    lines.append("| 我想 | 去这里 |")
    lines.append("|---|---|")
    lines.append("| 改任何数字 | `data/facts.yaml` |")
    lines.append("| 加新决议 | `data/decisions.yaml` + `meetings/YYYY-MM-DD-*.md` |")
    lines.append("| 改 BP 给投资人看 | `bps/store-front/bp.html` |")
    lines.append("| 查会议说过什么 | `meetings/` 目录 |")
    lines.append("| 看原始纪要/录屏 | `raw/meetings/` 目录 |")
    lines.append("| 改完跑校验 | `python tools/verify.py` |")
    lines.append("| 重出本图 | `python tools/render_directory.py --write` |")

    content = "\n".join(lines)

    if "--write" in sys.argv:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已写入 {OUTPUT_PATH}")
    else:
        print(content)


if __name__ == "__main__":
    main()
