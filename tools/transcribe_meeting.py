#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会议转录工具 (transcribe_meeting.py)
=====================================
用 faster-whisper (CUDA) 转录音频，输出：
1. SRT 字幕（含时间戳）
2. 纯文本（带时间戳）
3. JSON（含分段 + 置信度）

模型选择（速度 vs 准确度）：
- tiny:  最快，中文勉强
- base:  快，中文够用
- small: 平衡（推荐）~ 2GB VRAM
- medium: 准确，~ 5GB VRAM
- large-v3:  最准，~ 10GB VRAM（你 8GB 显存可能爆）

用法：
    python tools/transcribe_meeting.py --meeting 2026-06-26 --model medium
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "raw" / "meetings"


def format_timestamp(seconds):
    """秒 → HH:MM:SS.mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def srt_timestamp(seconds):
    """秒 → SRT 格式 HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def log(msg, log_file=None):
    """打印并写日志"""
    print(msg, flush=True)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")


def transcribe(meeting_date, model_name="small", language="zh"):
    """转录会议"""
    audio_path = RAW_DIR / meeting_date / "录屏" / "audio.wav"
    if not audio_path.exists():
        log(f"❌ 找不到音频文件：{audio_path}")
        log(f"   请先跑：python tools/extract_meeting.py --meeting {meeting_date}")
        return False
    
    out_dir = audio_path.parent
    log_file = out_dir / "transcribe.log"
    if log_file.exists():
        log_file.unlink()
    
    log(f"=== 转录会议 {meeting_date} ===", log_file)
    log(f"  模型：{model_name} | 语言：{language} | 设备：CUDA", log_file)
    log(f"  音频：{audio_path} ({audio_path.stat().st_size / 1024 / 1024:.0f} MB)", log_file)
    log("", log_file)
    
    # 加载模型
    log(f"[1/3] 加载 Whisper {model_name}（首次会下载模型）...", log_file)
    try:
        model = WhisperModel(model_name, device="cuda", compute_type="int8_float16")
    except Exception as e:
        log(f"  CUDA 加载失败，尝试 CPU：{e}", log_file)
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
    log(f"  ✅ 模型加载完成", log_file)
    log("", log_file)
    
    # 转录（带进度）
    log(f"[2/3] 开始转录（4小时会议预计 10-30 分钟）...", log_file)
    start = datetime.now()
    
    segments_iter, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        word_timestamps=False,
    )
    log(f"  音频时长：{info.duration:.0f}s | 语言：{info.language} (prob={info.language_probability:.2f})", log_file)
    log("", log_file)
    
    # 收集分段（带进度）
    seg_list = []
    last_print = 0
    log(f"[3/3] 转录中（每 60 秒打印一次进度）...", log_file)
    log(f"  开始时间：{datetime.now().strftime('%H:%M:%S')}", log_file)
    log(f"  日志文件：{log_file}", log_file)
    log("", log_file)
    
    for seg in segments_iter:
        seg_list.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip(),
            "avg_logprob": seg.avg_logprob,
            "no_speech_prob": seg.no_speech_prob,
        })
        now = datetime.now()
        # 每 5 段或每 30 秒打印一次（比之前激进）
        if len(seg_list) % 5 == 0 or (now - last_print).total_seconds() > 30:
            pct = (seg.end / info.duration * 100) if info.duration else 0
            msg = f"  [{datetime.now().strftime('%H:%M:%S')}] {pct:.1f}% | {len(seg_list)} 段 | {seg.end:.0f}s / {info.duration:.0f}s"
            log(msg, log_file)
            log(f"    最新: {seg.text[:80]}", log_file)
            last_print = now
    
    elapsed = (datetime.now() - start).total_seconds()
    speed = info.duration / elapsed if elapsed else 0
    log("", log_file)
    log(f"  ✅ 转录完成：{len(seg_list)} 段，耗时 {elapsed:.0f}s（{speed:.1f}x 实时）", log_file)
    
    # 写 JSON（机器读）
    json_path = out_dir / "transcript.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "meeting_date": meeting_date,
            "model": model_name,
            "language": info.language,
            "duration_sec": info.duration,
            "segment_count": len(seg_list),
            "segments": seg_list,
        }, f, ensure_ascii=False, indent=2)
    log(f"  📄 JSON: {json_path.name} ({json_path.stat().st_size / 1024:.1f} KB)", log_file)
    
    # 写 SRT 字幕（视频播放用）
    srt_path = out_dir / "transcript.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(seg_list, 1):
            f.write(f"{i}\n")
            f.write(f"{srt_timestamp(seg['start'])} --> {srt_timestamp(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")
    log(f"  📄 SRT: {srt_path.name} ({srt_path.stat().st_size / 1024:.1f} KB)", log_file)
    
    # 写带时间戳的纯文本（人读用）
    txt_path = out_dir / "transcript.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"# 会议转录 {meeting_date}\n")
        f.write(f"# 模型：{model_name} | 时长：{info.duration:.0f}s | 段数：{len(seg_list)}\n\n")
        for seg in seg_list:
            f.write(f"[{format_timestamp(seg['start'])}] {seg['text']}\n")
    log(f"  📄 TXT: {txt_path.name} ({txt_path.stat().st_size / 1024:.1f} KB)", log_file)
    
    log("", log_file)
    log(f"=== 转录完成 ===", log_file)
    log(f"  音频：{audio_path}", log_file)
    log(f"  段数：{len(seg_list)}", log_file)
    log(f"  下一步：python tools/split_speakers.py --meeting {meeting_date}", log_file)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--meeting", required=True, help="会议日期 YYYY-MM-DD")
    parser.add_argument("--model", default="small",
                       choices=["tiny", "base", "small", "medium", "large-v3"],
                       help="Whisper 模型大小")
    parser.add_argument("--language", default="zh", help="语言代码")
    args = parser.parse_args()
    sys.exit(0 if transcribe(args.meeting, args.model, args.language) else 1)
