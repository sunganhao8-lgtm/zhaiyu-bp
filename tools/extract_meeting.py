#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会议全流程处理工具 (extract_meeting.py)
==========================================
从腾讯会议录屏中提取：
1. 音频 WAV（用于 Whisper 转录）
2. 关键帧截图（用于查看 PPT/表格/手势）
3. 元数据（时长、采样率等）

用法：
    python tools/extract_meeting.py --meeting 2026-06-26
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "raw" / "meetings"


def find_recording(meeting_date):
    """找录屏文件"""
    candidates = list(RAW_DIR.glob(f"{meeting_date}*/录屏/meeting.mp4"))
    candidates += list(RAW_DIR.glob(f"{meeting_date}*/meeting*.mp4"))
    candidates += list(RAW_DIR.glob(f"{meeting_date}*/录屏/*.mp4"))
    if not candidates:
        return None
    # 优先取 meeting.mp4
    for c in candidates:
        if c.name == "meeting.mp4":
            return c
    return candidates[0]


def extract_audio(video_path, audio_path):
    """从视频中提取音频为 16kHz mono WAV（Whisper 最佳输入）"""
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000",
        "-c:a", "pcm_s16le",
        str(audio_path)
    ]
    print(f"  [audio] ffmpeg ...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [audio] FAIL: {r.stderr[-500:]}")
        return False
    size_mb = audio_path.stat().st_size / 1024 / 1024
    print(f"  [audio] OK: {size_mb:.1f} MB")
    return True


def extract_keyframes(video_path, frames_dir, interval_sec=30, max_frames=None):
    """每隔 N 秒抽一帧（关键帧采样）"""
    frames_dir.mkdir(parents=True, exist_ok=True)
    # 获取总时长
    cmd_duration = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
    ]
    duration = float(subprocess.check_output(cmd_duration).decode().strip())
    total = int(duration / interval_sec)
    if max_frames:
        total = min(total, max_frames)
    print(f"  [frames] duration={duration:.0f}s, extracting {total} frames @ every {interval_sec}s")
    
    # 用 ffmpeg 每 N 秒抽一帧
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", f"fps=1/{interval_sec}",
        "-q:v", "2",  # 高质量 JPEG
        str(frames_dir / "frame_%04d.jpg")
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [frames] FAIL: {r.stderr[-500:]}")
        return 0
    
    # 统计实际抽到的帧
    actual = len(list(frames_dir.glob("frame_*.jpg")))
    print(f"  [frames] OK: {actual} frames extracted to {frames_dir.name}/")
    return actual


def extract_meeting(meeting_date, interval_sec=30):
    """主函数"""
    print(f"=== 提取会议 {meeting_date} ===\n")
    
    video = find_recording(meeting_date)
    if not video:
        print(f"❌ 找不到录屏文件（请把 mp4 放到 raw/meetings/{meeting_date}*/录屏/）")
        return False
    
    print(f"📹 录屏文件：{video}")
    print(f"   大小：{video.stat().st_size / 1024 / 1024:.1f} MB\n")
    
    out_dir = video.parent
    audio_path = out_dir / "audio.wav"
    frames_dir = out_dir / "frames"
    meta_path = out_dir / "extract_meta.json"
    
    # 1. 抽音频
    print("[1/3] 提取音频（16kHz mono WAV）")
    if not extract_audio(video, audio_path):
        return False
    
    # 2. 抽关键帧
    print("\n[2/3] 提取关键帧（每 {} 秒）".format(interval_sec))
    n_frames = extract_keyframes(video, frames_dir, interval_sec)
    if n_frames == 0:
        print("❌ 抽帧失败")
        return False
    
    # 3. 写元数据
    print("\n[3/3] 写元数据")
    duration_sec = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video)
    ]).decode().strip())
    
    meta = {
        "meeting_date": meeting_date,
        "source_video": str(video.relative_to(ROOT)),
        "audio_file": str(audio_path.relative_to(ROOT)),
        "frames_dir": str(frames_dir.relative_to(ROOT)),
        "frame_count": n_frames,
        "frame_interval_sec": interval_sec,
        "duration_sec": duration_sec,
        "duration_human": f"{int(duration_sec // 3600)}h {int(duration_sec % 3600 // 60)}m {int(duration_sec % 60)}s",
        "extracted_at": datetime.now().isoformat(),
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ 元数据：{meta_path}")
    print(f"\n=== 提取完成 ===")
    print(f"  音频：{audio_path} ({audio_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"  帧数：{n_frames} 张")
    print(f"  下一步：python tools/transcribe_meeting.py --meeting {meeting_date}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--meeting", required=True, help="会议日期 YYYY-MM-DD")
    parser.add_argument("--interval", type=int, default=30, help="抽帧间隔（秒）")
    args = parser.parse_args()
    sys.exit(0 if extract_meeting(args.meeting, args.interval) else 1)
