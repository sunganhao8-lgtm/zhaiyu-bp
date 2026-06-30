#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书妙记转写稿 → 项目会议笔记转换器
=============================================
支持输入：飞书妙记导出的 SRT / TXT / Word
输出：raw/meetings/{date}/transcript_normalized.{json,txt,srt}

用法：
  python tools/import_feishu_minutes.py --input 下载文件路径 --date 2026-06-26 --speakers 孙淦浩,陈老师
"""
import argparse, json, re, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw" / "meetings"


def srt_time_to_sec(t: str) -> float:
    """00:01:23,456 -> 83.456"""
    h, m, rest = t.strip().split(":")
    s, ms = rest.split(",")
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000


def parse_srt(path: Path) -> list:
    """解析 SRT 文件，返回 [{start, end, text, speaker}]"""
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", text.strip())
    segs = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+)\s+([\d:,]+)\s*-->\s*([\d:,]+)", lines[0])
        if not m:
            continue
        segs.append({
            "start": srt_time_to_sec(m.group(2)),
            "end": srt_time_to_sec(m.group(3)),
            "text": " ".join(x.strip() for x in lines[2:]),
            "speaker": None,
        })
    return segs


def parse_txt(path: Path) -> list:
    """解析飞书导出的 TXT（带时间戳行 [00:12:34]）
    返回 [{start, end, text, speaker}]
    """
    text = path.read_text(encoding="utf-8")
    segs = []
    pattern = re.compile(r"\[(\d{1,2}):(\d{2}):(\d{2})\]\s*(.*)")
    for line in text.splitlines():
        m = pattern.match(line.strip())
        if m:
            h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
            sec = h*3600 + mi*60 + s
            segs.append({
                "start": sec,
                "end": sec + 5,  # TXT 通常没 end，估 5 秒
                "text": m.group(4).strip(),
                "speaker": None,
            })
    # 如果没有时间戳，fallback：按空行分块
    if not segs:
        chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
        segs = [{"start": i*10, "end": (i+1)*10, "text": c, "speaker": None}
                for i, c in enumerate(chunks)]
    return segs


def fmt_ts(sec: float) -> str:
    h = int(sec // 3600); m = int((sec % 3600) // 60); s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def save_outputs(segs: list, out_dir: Path, date: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    # JSON
    j = {
        "meeting_date": date,
        "source": "feishu-minutes",
        "segment_count": len(segs),
        "speakers": list({s for s in (x.get("speaker") for x in segs) if s}),
        "segments": segs,
    }
    (out_dir / "transcript_normalized.json").write_text(
        json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    # TXT
    lines = [f"# 会议转写 {date}\n# 来源：飞书妙记\n# 段数：{len(segs)}\n"]
    for seg in segs:
        sp = f"[{seg['speaker']}] " if seg.get("speaker") else ""
        lines.append(f"[{fmt_ts(seg['start'])}] {sp}{seg['text']}")
    (out_dir / "transcript_normalized.txt").write_text("\n".join(lines), encoding="utf-8")
    # Markdown 摘要（人读用）
    md = [f"# {date} 会议转写\n", f"> 来源：飞书妙记 | 段数：{len(segs)}\n"]
    current_sp = None
    for seg in segs:
        sp = seg.get("speaker") or "（未标注）"
        if sp != current_sp:
            md.append(f"\n## {sp}\n")
            current_sp = sp
        md.append(f"- [{fmt_ts(seg['start'])}] {seg['text']}")
    (out_dir / "transcript_normalized.md").write_text("\n".join(md), encoding="utf-8")
    print(f"  ✅ 输出到：{out_dir}")
    print(f"     JSON: {(out_dir/'transcript_normalized.json').stat().st_size//1024} KB")
    print(f"     TXT:  {(out_dir/'transcript_normalized.txt').stat().st_size//1024} KB")
    print(f"     MD:   {(out_dir/'transcript_normalized.md').stat().st_size//1024} KB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="飞书妙记导出文件路径（SRT/TXT）")
    ap.add_argument("--date", required=True)
    ap.add_argument("--speakers", default="", help="逗号分隔列表，用于后续标注（孙淦浩,陈老师...）")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"❌ 找不到文件：{src}")
        sys.exit(1)

    fmt = src.suffix.lower()
    print(f"输入：{src} ({fmt})")
    if fmt == ".srt":
        segs = parse_srt(src)
    elif fmt in (".txt", ".md"):
        segs = parse_txt(src)
    else:
        print(f"❌ 不支持格式：{fmt}（仅支持 .srt / .txt）")
        sys.exit(1)

    print(f"  解析到 {len(segs)} 段")
    out = RAW / args.date / "录屏"
    save_outputs(segs, out, args.date)
    print("\n下一步：手动为说话人标注（edit transcript_normalized.json）")


if __name__ == "__main__":
    main()
