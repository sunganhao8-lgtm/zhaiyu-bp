#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重建会议笔记 v2 — 固定章节解析 (fix regex)"""
import re, json, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(r"C:\Users\11390\Desktop\zhaiyu-bp")
DATE = "2026-06-26"
SRC = ROOT / "raw" / "meetings" / DATE / "飞书妙记_原始导出.md"
OUT_MD = ROOT / "meetings" / f"{DATE}-孙淦浩快速会议.md"
OUT_JSON = ROOT / "raw" / "meetings" / DATE / "transcript_labeled.json"

SPEAKER_MAP = {
    "1": "张显坤",
    "2": "陈老师",
    "3": "孙淦浩",
    "6": "原店铺主人",
}

def extract_action_items(text: str):
    items = []
    in_section = False
    for line in text.splitlines():
        if line.strip() == "# 待办":
            in_section = True
            continue
        if in_section:
            if line.startswith("# "):
                break
            if line.strip().startswith("- [ ]"):
                items.append(line.strip()[5:].strip())
    return items

def extract_chapters(text: str):
    chapters = []
    lines = text.splitlines()

    # 找 "智能章节" 章节起始位置
    start_idx = 0
    for idx, line in enumerate(lines):
        if line.strip() == "# 智能章节":
            start_idx = idx + 1
            break

    current = None
    chapter_re = re.compile(r'^\[([0-9]{2}:[0-9]{2})\]\([^)]*\)\*{2}\s+(.+?)\*{2}$')

    for i in range(start_idx, len(lines)):
        line = lines[i].rstrip()

        # 新章节：\\[HH:MM\\](url)**  标题**
        m = chapter_re.match(line)
        if m:
            if current and current["summary"].strip():
                chapters.append(current)
            current = {
                "time": m.group(1),
                "title": m.group(2).strip(),
                "summary": "",
                "utterances": [],
            }
            continue

        # 逐句转写："说话人N: 内容" 或 "说话人N：内容"
        ms = re.match(r'^(说话人\s*\d+)[：:]\s*(.+)$', line)
        if ms and current is not None:
            spk = re.search(r'\d+', ms.group(1)).group()
            current["utterances"].append({
                "speaker": spk,
                "speaker_name": SPEAKER_MAP.get(spk, f"说话人{spk}"),
                "text": ms.group(2).strip(),
            })
            continue

        # 章节摘要：> 开头
        if line.startswith("> ") and current is not None:
            content = line.lstrip("> ").strip()
            if content:
                current["summary"] += content + "\n"
            continue

        # 遇到新的 top-level section 中止
        if line.startswith("# ") and current is not None:
            break

    if current and current["summary"].strip():
        chapters.append(current)

    return chapters

def main():
    text = SRC.read_text(encoding="utf-8")
    action_items = extract_action_items(text)
    chapters = extract_chapters(text)

    # 渲染 Markdown
    out_lines = []
    out_lines.append("# 2026-06-26 孙淦浩快速会议（飞书妙记 v2.0 · 精确说话人版）\n")
    out_lines.append("> **转录来源**：飞书妙记自动转录")
    out_lines.append(f"> **原始文件**：`raw/meetings/{DATE}/飞书妙记_原始导出.md`")
    out_lines.append("> **说话人映射**：")
    for k, v in SPEAKER_MAP.items():
        out_lines.append(f"> - 说话人 {k} → **{v}**")
    out_lines.append("> ⚠️ 同房间同设备，基于上下文推断，待人工二次确认。\n")
    out_lines.append("---\n")

    out_lines.append("## 一、待办事项\n")
    for item in action_items:
        out_lines.append(f"- [ ] {item}")
    out_lines.append("")

    out_lines.append("## 二、智能章节（按时间）\n")
    for ch in chapters:
        out_lines.append(f"### {ch['time']} {ch['title']}\n")
        summary_text = ch["summary"].strip()
        if summary_text:
            out_lines.append(f"> **章节摘要**：\n> {summary_text}\n")
        if ch.get("utterances"):
            out_lines.append("**逐句转写**：\n")
            for u in ch["utterances"]:
                out_lines.append(f"- **[{u['speaker_name']}]** {u['text']}")
        out_lines.append("")

    out_lines.append("## 三、说话人归属（待确认）\n")
    out_lines.append("| 说话人 | 推断姓名 | 关键证据 |")
    out_lines.append("|--------|----------|----------|")
    evidence = {
        "1": ("张显坤", "被要求发表格、提到PC经验、被呼唤'坤坤'"),
        "2": ("陈老师", "认可方案、负责群运营、'对象做店内接待'"),
        "3": ("孙淦浩", "主导决策、呼唤坤坤、'少投1000'、'机制健康'"),
        "6": ("原店铺主人", "转让事宜、保证无涨租、谈价6万"),
    }
    for k in sorted(SPEAKER_MAP.keys()):
        name, ev = evidence.get(k, ("???", ""))
        out_lines.append(f"| 说话人 {k} | {name} | {ev} |")
    out_lines.append("\n---\n*本笔记由 `tools/rebuild_meeting_notes.py` v2 自动生成。说话人映射需人工确认。*\n")

    OUT_MD.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"[1/2] 会议笔记已写入：{OUT_MD}")
    print(f"       章节: {len(chapters)} / 待办: {len(action_items)} / 大小: {OUT_MD.stat().st_size} 字节")

    payload = {
        "source": str(SRC),
        "parsed_at": datetime.now().isoformat(),
        "total_chapters": len(chapters),
        "speaker_map": SPEAKER_MAP,
        "action_items": action_items,
        "chapters": chapters,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[2/2] 转写 JSON：{OUT_JSON}")

if __name__ == "__main__":
    main()
