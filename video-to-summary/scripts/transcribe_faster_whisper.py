#!/usr/bin/env python3
"""
transcribe_faster_whisper.py — faster-whisper ASR 后端转写

用法:
    python3 transcribe_faster_whisper.py <音频文件> --output_dir <目录> [选项]

依赖:
    pip install faster-whisper ctranslate2
"""

import argparse
import os
import sys
import time


def main():
    parser = argparse.ArgumentParser(description="faster-whisper 转写")
    parser.add_argument("audio", help="音频文件路径")
    parser.add_argument("--output_dir", "-o", default=".", help="输出目录")
    parser.add_argument("--model_size", default="small",
                        help="模型大小: tiny/base/small/medium/large-v3")
    parser.add_argument("--device", default="auto", help="auto/cpu/cuda")
    parser.add_argument("--compute_type", default="", help="如 float16")
    parser.add_argument("--language", default="zh", help="语言代码")
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"❌ 文件不存在: {args.audio}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.audio))[0]

    # 设备自动检测
    device = args.device
    if device == "auto":
        try:
            import subprocess
            result = subprocess.run(
                ["python3", "-c", "import torch; print(torch.cuda.is_available())"],
                capture_output=True, text=True, timeout=10
            )
            device = "cuda" if result.stdout.strip() == "True" else "cpu"
        except Exception:
            device = "cpu"

    compute_type = args.compute_type
    if not compute_type:
        compute_type = "float16" if device == "cuda" else "int8"

    print(f"🔊 加载 faster-whisper ({args.model_size}, {device}, {compute_type})...")
    t0 = time.time()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("❌ 请先安装: pip install faster-whisper ctranslate2", file=sys.stderr)
        sys.exit(1)

    model = WhisperModel(args.model_size, device=device, compute_type=compute_type)

    print(f"🎤 转写中 (语言: {args.language or 'auto'})...")
    segments, info = model.transcribe(args.audio, language=args.language or None, beam_size=5)

    # 收集结果
    all_text = []
    srt_lines = []
    srt_idx = 1

    for seg in segments:
        all_text.append(seg.text.strip())

        # SRT 格式
        start_s = int(seg.start)
        start_ms = int((seg.start - start_s) * 1000)
        end_s = int(seg.end)
        end_ms = int((seg.end - end_s) * 1000)

        start_fmt = f"{start_s//3600:02d}:{(start_s%3600)//60:02d}:{start_s%60:02d},{start_ms:03d}"
        end_fmt = f"{end_s//3600:02d}:{(end_s%3600)//60:02d}:{end_s%60:02d},{end_ms:03d}"

        srt_lines.append(str(srt_idx))
        srt_lines.append(f"{start_fmt} --> {end_fmt}")
        srt_lines.append(seg.text.strip())
        srt_lines.append("")
        srt_idx += 1

    elapsed = time.time() - t0
    full_text = "\n".join(all_text)

    # 写入文件
    txt_path = os.path.join(args.output_dir, f"{base}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    srt_path = os.path.join(args.output_dir, f"{base}.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    print(f"\n✅ 转写完成! 耗时 {elapsed:.0f} 秒")
    print(f"   文本: {txt_path} ({len(full_text)} 字符)")
    print(f"   字幕: {srt_path}")


if __name__ == "__main__":
    main()
