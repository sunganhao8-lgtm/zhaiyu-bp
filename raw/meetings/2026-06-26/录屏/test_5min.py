#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速测试转录：只跑前 5 分钟看效果"""
import sys
from pathlib import Path
from faster_whisper import WhisperModel

AUDIO = Path(r"C:\Users\11390\Desktop\zhaiyu-bp\raw\meetings\2026-06-26\录屏\audio_test5min.wav")
LOG = AUDIO.parent / "test_5min.log"

def main():
    with open(LOG, "w", encoding="utf-8") as log:
        log.write("加载模型...\n"); log.flush()
        model = WhisperModel("small", device="cuda", compute_type="int8_float16")
        log.write("模型就绪，开始转录前 5 分钟\n"); log.flush()
        
        segs, info = model.transcribe(
            str(AUDIO),
            language="zh",
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            word_timestamps=True,  # 测试时打开，拿到词级时间戳
        )
        log.write(f"音频时长: {info.duration}s\n"); log.flush()
        
        count = 0
        for seg in segs:
            count += 1
            log.write(f"[{seg.start:.1f}s -> {seg.end:.1f}s] {seg.text}\n"); log.flush()
            if count <= 5 and seg.words:
                for w in seg.words:
                    log.write(f"    word [{w.start:.2f}-{w.end:.2f}] {w.word} (prob={w.probability:.2f})\n")
                log.flush()
        log.write(f"完成: {count} 段\n")

if __name__ == "__main__":
    main()
