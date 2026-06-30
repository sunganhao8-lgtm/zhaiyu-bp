#!/usr/bin/env python3
"""
宅域 INDEX 自动生成器 (render_index.py)
=======================================
扫描项目目录，自动生成 INDEX.md。

用法：
    python tools/render_index.py          # 输出到终端
    python tools/render_index.py --write  # 写入 INDEX.md
"""

import os
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {".git", "__pycache__", "node_modules"}

def get_file_info(path):
    """获取文件的基本信息"""
    stat = os.stat(path)
    size = stat.st_size
    if size < 1024:
        size_str = f"{size}B"
    elif size < 1024 * 1024:
        size_str = f"{size/1024:.0f}KB"
    else:
        size_str = f"{size/1024/1024:.1f}MB"
    
    mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
    return size_str, mtime


def scan_meetings():
    """扫描 meetings/ 目录"""
    path = os.path.join(ROOT, "meetings")
    if not os.path.isdir(path):
        return []
    items = []
    for f in sorted(os.listdir(path), reverse=True):
        if f.startswith("_") or not f.endswith(".md"):
            continue
        fpath = os.path.join(path, f)
        size_str, mtime = get_file_info(fpath)
        
        # 从文件内容读第一行标题
        title = f.replace(".md", "")
        with open(fpath, "r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if line.startswith("# ") and not line.startswith("##"):
                    title = line[2:].strip()
                    break
        
        items.append((f, title, mtime, size_str))
    return items


def collect_dir(name, path, extensions=None):
    """扫描某个目录"""
    if not os.path.isdir(path):
        return []
    items = []
    for f in sorted(os.listdir(path)):
        if f.startswith("."):
            continue
        fpath = os.path.join(path, f)
        if os.path.isfile(fpath):
            if extensions and not any(f.endswith(e) for e in extensions):
                continue
            size_str, mtime = get_file_info(fpath)
            items.append((f, mtime, size_str))
        elif os.path.isdir(fpath):
            # Count files inside
            count = sum(1 for root, dirs, files in os.walk(fpath) 
                       for fname in files if not fname.startswith("."))
            items.append((f + "/", "", f"{count} files"))
    return items


def generate_index():
    """生成 INDEX.md 内容"""
    parts = []
    
    parts.append(f"# 宅域 — 知识库索引\n")
    parts.append(f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    parts.append(f"> 运行 `python tools/render_index.py --write` 更新\n")
    parts.append(f"---\n")
    
    # ── 会议笔记 ──
    meetings = scan_meetings()
    if meetings:
        parts.append("## 📝 会议笔记\n")
        parts.append("| 文件 | 主题 | 日期 | 大小 |")
        parts.append("|---|---|---|---|")
        for fname, title, mtime, size in meetings:
            parts.append(f"| [[meetings/{fname}]] | {title} | {mtime} | {size} |")
        parts.append("")
    
    # ── 数据源 ──
    parts.append("## 📊 数据源\n")
    data_items = collect_dir("data/", os.path.join(ROOT, "data"))
    if data_items:
        parts.append("| 文件 | 更新 | 大小 |")
        parts.append("|---|---|---|")
        for fname, mtime, size in data_items:
            parts.append(f"| [[data/{fname}]] | {mtime} | {size} |")
        parts.append("")
    
    # ── 业务交付物 ──
    parts.append("## 📦 业务交付物\n")
    bps_path = os.path.join(ROOT, "bps")
    if os.path.isdir(bps_path):
        for sub in sorted(os.listdir(bps_path)):
            subpath = os.path.join(bps_path, sub)
            if not os.path.isdir(subpath) or sub.startswith("."):
                continue
            
            # Read README for description
            readme_path = os.path.join(subpath, "README.md")
            desc = ""
            if os.path.isfile(readme_path):
                with open(readme_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            desc = line[:100]
                            break
            
            parts.append(f"### {sub}")
            if desc:
                parts.append(f"> {desc}")
            
            items = collect_dir(f"bps/{sub}", subpath, extensions=[".html", ".md"])
            if items:
                parts.append("| 文件 | 更新 | 大小 |")
                parts.append("|---|---|---|")
                for fname, mtime, size in items:
                    parts.append(f"| [[bps/{sub}/{fname}]] | {mtime} | {size} |")
            parts.append("")
    
    # ── 原始素材 ──
    parts.append("## 📄 原始素材\n")
    raw_path = os.path.join(ROOT, "raw")
    if os.path.isdir(raw_path):
        for sub in sorted(os.listdir(raw_path)):
            subpath = os.path.join(raw_path, sub)
            if not os.path.isdir(subpath) or sub.startswith("."):
                continue
            parts.append(f"### {sub}")
            items = collect_dir(f"raw/{sub}", subpath)
            if items:
                parts.append("| 文件 | 更新 | 大小 |")
                parts.append("|---|---|---|")
                for fname, mtime, size in items:
                    parts.append(f"| [{fname}](raw/{sub}/{fname}) | {mtime} | {size} |")
            parts.append("")
    
    # ── 归档 ──
    arch_path = os.path.join(ROOT, "archive")
    if os.path.isdir(arch_path):
        parts.append("## 🗄️ 归档\n")
        for sub in sorted(os.listdir(arch_path)):
            subpath = os.path.join(arch_path, sub)
            if not os.path.isdir(subpath) or sub.startswith("."):
                continue
            count = sum(1 for root, dirs, files in os.walk(subpath) for f in files if not f.startswith("."))
            parts.append(f"- **{sub}** — {count} 个工作文件")
        parts.append("")
    
    # ── 工具 ──
    parts.append("## 🔧 工具\n")
    tool_path = os.path.join(ROOT, "tools")
    if os.path.isdir(tool_path):
        for f in sorted(os.listdir(tool_path)):
            if f.endswith(".py") or f.endswith(".sh"):
                fpath = os.path.join(tool_path, f)
                size_str, mtime = get_file_info(fpath)
                # Read first few lines for description
                with open(fpath, "r", encoding="utf-8") as fp:
                    first_lines = [fp.readline().strip() for _ in range(5)]
                desc_line = next((l for l in first_lines if l.startswith("# ") and not l.startswith("#!/")), "")
                desc = desc_line[2:].strip() if desc_line else ""
                parts.append(f"- **[{f}](tools/{f})** — {desc} ({size_str})")
        parts.append("")
    
    # ── 统计 ──
    all_files = sum(1 for root, dirs, files in os.walk(ROOT) 
                    if not any(d in SKIP_DIRS for d in root.split(os.sep))
                    for f in files if not f.startswith("."))
    parts.append(f"---\n")
    parts.append(f"> 📊 总计 {all_files} 个文件 | 最后更新 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    return "\n".join(parts)


if __name__ == "__main__":
    index = generate_index()
    
    if "--write" in sys.argv:
        output_path = os.path.join(ROOT, "INDEX.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(index)
        print(f"OK: wrote {output_path}")
    else:
        print(index)
