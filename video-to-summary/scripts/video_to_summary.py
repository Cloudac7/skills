#!/usr/bin/env python3
"""
video_to_summary.py — 视频下载→转写→总结 全流程自动化

支持平台: B站、YouTube、抖音/TikTok、小红书、本地视频/音频文件

用法:
    # 查看信息
    python3 video_to_summary.py info <URL>

    # 完整流水线（下载+转写）
    python3 video_to_summary.py pipeline <URL> -o <输出目录>

    # 转写本地文件
    python3 video_to_summary.py transcribe <本地文件> -o <输出目录>
"""

import argparse
import os
import subprocess
import sys
import re
import urllib.parse

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BD_SCRIPT = os.path.join(SKILL_DIR, "..", "..", "bilibili-downloader-plus", "scripts", "bilibili_download.py")


def detect_platform(url_or_path: str) -> str:
    """检测输入类型: bilibili / youtube / douyin / xiaohongshu / local_video / local_audio"""
    if os.path.exists(url_or_path):
        ext = os.path.splitext(url_or_path)[1].lower()
        if ext in (".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma"):
            return "local_audio"
        return "local_video"

    url = url_or_path.lower()
    if any(d in url for d in ["bilibili.com", "b23.tv"]):
        return "bilibili"
    if any(d in url for d in ["youtube.com", "youtu.be"]):
        return "youtube"
    if any(d in url for d in ["douyin.com", "tiktok.com"]):
        return "douyin"
    if any(d in url for d in ["xiaohongshu.com", "xhslink.com"]):
        return "xiaohongshu"
    return "unknown"


def find_video_file(directory: str) -> str | None:
    """在目录中查找视频文件"""
    for f in os.listdir(directory):
        if f.endswith((".mp4", ".mkv", ".webm", ".mov")):
            return os.path.join(directory, f)
    return None


def cmd_info(args):
    """查看视频信息"""
    platform = detect_platform(args.url)

    if platform == "bilibili":
        bd_script = os.path.abspath(BD_SCRIPT)
        if not os.path.exists(bd_script):
            print("❌ 找不到 bilibili_download.py", file=sys.stderr)
            sys.exit(1)
        result = subprocess.run([sys.executable, bd_script, "info", args.url])
        sys.exit(result.returncode)

    elif platform == "youtube":
        result = subprocess.run([
            "yt-dlp", "--print", "%(title)s", "--print", "%(duration)s",
            "--print", "%(channel)s", "--no-download", args.url
        ])
        sys.exit(result.returncode)

    elif platform in ("douyin", "xiaohongshu"):
        result = subprocess.run([
            "yt-dlp", "--print", "%(title)s", "--print", "%(duration)s",
            "--print", "%(uploader)s", "--no-download", args.url
        ])
        sys.exit(result.returncode)

    else:
        print(f"❌ 不支持的平台: {args.url}", file=sys.stderr)
        sys.exit(1)


def cmd_transcribe(args):
    """转写：视频/音频文件 → 文字"""
    source = args.source
    output_dir = os.path.abspath(args.output) if args.output else os.path.dirname(source)
    model = args.model or "medium"

    if not os.path.exists(source):
        print(f"❌ 文件不存在: {source}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(source))[0]

    # 提取音频（如果是视频文件）
    audio_file = source
    need_cleanup = False
    if os.path.splitext(source)[1].lower() in (".mp4", ".mkv", ".webm", ".mov", ".avi"):
        audio_file = os.path.join(output_dir, f"{base}_audio.mp3")
        if not os.path.exists(audio_file):
            print(f"🔊 提取音频: {os.path.basename(source)}")
            subprocess.run([
                "ffmpeg", "-i", source, "-q:a", "0", "-map", "a", "-y", audio_file
            ], check=True, capture_output=True)
            need_cleanup = True

    # 选择 ASR 后端
    asr_backend = os.environ.get("ASR_BACKEND", "whisper")

    if asr_backend == "faster-whisper":
        _transcribe_faster_whisper(audio_file, output_dir, model, args.language)
    else:
        _transcribe_whisper(audio_file, output_dir, model, args.language)

    # 清理临时音频
    if need_cleanup and os.path.exists(audio_file):
        os.remove(audio_file)

    # 列出输出文件
    print(f"\n✅ 转写完成! 输出文件:")
    for ext in ["txt", "srt", "vtt", "tsv", "json"]:
        fp = os.path.join(output_dir, f"{base}.{ext}")
        if os.path.exists(fp):
            size = os.path.getsize(fp)
            print(f"   📄 {base}.{ext} ({size/1024:.0f} KB)")

    return os.path.join(output_dir, f"{base}.txt")


def _transcribe_whisper(audio_file, output_dir, model, language):
    """使用 uvx openai-whisper 转写"""
    print(f"🎤 [whisper] 转写中 (model={model}, lang={language or 'auto'})...")

    whisper_cmd = [
        "uvx", "--from", "openai-whisper", "whisper",
        audio_file, "--model", model, "--output_dir", output_dir,
    ]
    if language:
        whisper_cmd.extend(["--language", language])

    try:
        subprocess.run(whisper_cmd, check=True)
    except subprocess.CalledProcessError as e:
        if "SHA256 checksum" in str(e):
            print("  模型校验失败, 清除缓存重试...")
            subprocess.run(["rm", "-f", os.path.expanduser(f"~/.cache/whisper/{model}.pt")])
            subprocess.run(whisper_cmd, check=True)
        else:
            raise


def _transcribe_faster_whisper(audio_file, output_dir, model, language):
    """使用 faster-whisper 转写"""
    fw_script = os.path.join(SKILL_DIR, "transcribe_faster_whisper.py")
    if not os.path.exists(fw_script):
        print("❌ 找不到 transcribe_faster_whisper.py", file=sys.stderr)
        sys.exit(1)

    device = os.environ.get("FW_DEVICE", "auto")
    compute = os.environ.get("FW_COMPUTE_TYPE", "")
    cmd = [
        "uvx", "--with", "faster-whisper", "--with", "ctranslate2",
        "python3", fw_script, audio_file,
        "--output_dir", output_dir,
        "--model_size", model,
        "--device", device,
    ]
    if compute:
        cmd.extend(["--compute_type", compute])
    if language:
        cmd.extend(["--language", language])

    subprocess.run(cmd, check=True)


def cmd_pipeline(args):
    """完整流水线：下载 → 转写"""
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)
    platform = detect_platform(args.url)

    print(f"🎯 检测平台: {platform}")

    # ---- 步骤1: 下载 ----
    print("=" * 50)
    print("步骤 1/3: 获取视频")
    print("=" * 50)

    video_path = None

    if platform == "bilibili":
        bd_script = os.path.abspath(BD_SCRIPT)
        if not os.path.exists(bd_script):
            print("❌ 找不到 bilibili_download.py", file=sys.stderr)
            sys.exit(1)

        bd_cmd = [sys.executable, bd_script, "download", args.url, "-o", output_dir]
        if args.browser:
            bd_cmd.extend(["--browser", args.browser])
        if args.collection:
            bd_cmd.append("--collection")

        result = subprocess.run(bd_cmd)
        if result.returncode != 0:
            print("❌ B站下载失败", file=sys.stderr)
            sys.exit(1)

        video_path = find_video_file(output_dir)
        if not video_path:
            for root, dirs, files in os.walk(output_dir):
                for f in files:
                    if f.endswith((".mp4", ".mkv", ".webm")):
                        video_path = os.path.join(root, f)
                        break
                if video_path:
                    break

    elif platform == "youtube":
        # 优先尝试抓字幕（不下载视频）
        print("📝 YouTube: 尝试直接抓取字幕...")
        subprocess.run([
            "yt-dlp", "--skip-download",
            "--write-auto-subs", "--write-subs",
            "--sub-langs", "zh-Hans,zh-Hant,zh,en",
            "--convert-subs", "srt",
            "-o", os.path.join(output_dir, "%(id)s/%(title)s.%(ext)s"),
            args.url
        ], capture_output=True)

        # 检查是否抓到了字幕
        found_sub = False
        for root, dirs, files in os.walk(output_dir):
            for f in files:
                if f.endswith((".srt", ".vtt")):
                    sub_path = os.path.join(root, f)
                    if os.path.getsize(sub_path) > 100:
                        print(f"  ✅ 抓到字幕: {sub_path}")
                        # 将字幕转换为纯文本
                        txt_path = os.path.join(output_dir, "subtitle.txt")
                        _convert_sub_to_text(sub_path, txt_path)
                        found_sub = True
                        break
            if found_sub:
                break

        if found_sub:
            print("\n✅ 字幕获取完成!")
            return

        # 字幕不可用 → 下载视频
        print("  ⚠️  无可用字幕，回退到下载+ASR 流程")
        result = subprocess.run([
            "yt-dlp", "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "--merge-output-format", "mp4",
            "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
            args.url
        ])
        if result.returncode != 0:
            print("❌ YouTube 下载失败", file=sys.stderr)
            sys.exit(1)
        video_path = find_video_file(output_dir)

    elif platform in ("douyin", "xiaohongshu"):
        result = subprocess.run([
            "yt-dlp", "-f", "best",
            "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
            args.url
        ])
        if result.returncode != 0:
            print(f"❌ {platform} 下载失败", file=sys.stderr)
            sys.exit(1)
        video_path = find_video_file(output_dir)

    else:
        print(f"❌ 不支持的输入: {args.url}", file=sys.stderr)
        sys.exit(1)

    if not video_path:
        print("❌ 找不到下载的视频文件", file=sys.stderr)
        sys.exit(1)

    print(f"  ✅ 视频: {os.path.basename(video_path)}")

    # ---- 步骤2: 转写 ----
    print("\n" + "=" * 50)
    print("步骤 2/3: 语音转写")
    print("=" * 50)

    txt_path = cmd_transcribe(argparse.Namespace(
        source=video_path,
        output=os.path.dirname(video_path),
        model=args.model,
        language=args.language,
    ))

    # ---- 步骤3: 总结提示 ----
    print("\n" + "=" * 50)
    print("步骤 3/3: 内容总结")
    print("=" * 50)

    if txt_path and os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"\n转写字数: {len(text)} 字")
        print(f"转写文本: {txt_path}")
        print("正在基于转写文本生成内容总结...")


def _convert_sub_to_text(sub_path: str, txt_path: str):
    """将 SRT/VTT 字幕文件转为纯文本"""
    import re
    with open(sub_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 去除时间轴行和序号行
    lines = []
    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue
        if re.match(r"^\d+$", line):
            continue
        if "-->" in line:
            continue
        if line.startswith("WEBVTT"):
            continue
        lines.append(line)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  📄 字幕转文本: {txt_path} ({len(''.join(lines))} 字符)")


def main():
    parser = argparse.ArgumentParser(description="视频 下载→转写→总结 流水线")
    sub = parser.add_subparsers(dest="command")

    # info
    p_info = sub.add_parser("info", help="查看视频信息")
    p_info.add_argument("url", help="视频 URL")

    # transcribe
    p_tr = sub.add_parser("transcribe", help="转写本地视频/音频文件")
    p_tr.add_argument("source", help="视频或音频文件路径")
    p_tr.add_argument("-o", "--output", help="输出目录（默认源文件所在目录）")
    p_tr.add_argument("--model", default="medium", help="whisper 模型")
    p_tr.add_argument("--language", default="zh", help="语言代码")

    # pipeline
    p_pl = sub.add_parser("pipeline", help="完整流水线")
    p_pl.add_argument("url", help="视频 URL")
    p_pl.add_argument("-o", "--output", required=True, help="输出目录")
    p_pl.add_argument("-b", "--browser", default="", help="浏览器 (chrome/edge/firefox, 仅B站)")
    p_pl.add_argument("-c", "--collection", action="store_true", help="下载整个合集 (仅B站)")
    p_pl.add_argument("--model", default="medium", help="whisper 模型")
    p_pl.add_argument("--language", default="zh", help="语言代码")

    args = parser.parse_args()

    if args.command == "info":
        cmd_info(args)
    elif args.command == "transcribe":
        cmd_transcribe(args)
    elif args.command == "pipeline":
        cmd_pipeline(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
