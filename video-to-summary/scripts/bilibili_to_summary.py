#!/usr/bin/env python3
"""
bilibili_to_summary.py — B站视频下载→转写→总结 全流程自动化

用法:
    # 查看信息
    python3 bilibili_to_summary.py info <BILIBILI_URL>

    # 完整流水线（下载+转写+输出文字路径）
    python3 bilibili_to_summary.py pipeline <BILIBILI_URL> -o <输出目录>

    # 仅转写（视频已存在）
    python3 bilibili_to_summary.py transcribe <视频文件.mp4> -o <输出目录>
"""

import argparse
import json
import os
import subprocess
import sys
import shutil

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BD_SCRIPT = os.path.join(SKILL_DIR, "..", "..", "bilibili-downloader-plus", "scripts", "bilibili_download.py")


def find_video_file(directory: str) -> str | None:
    """在目录中查找 .mp4 文件"""
    for f in os.listdir(directory):
        if f.endswith(".mp4"):
            return os.path.join(directory, f)
    return None


def cmd_info(args):
    """查看视频信息"""
    bd_script = os.path.abspath(BD_SCRIPT)
    if not os.path.exists(bd_script):
        print("❌ 找不到 bilibili_download.py，请确认 bilibili-downloader-plus 技能已安装", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run([sys.executable, bd_script, "info", args.url])
    sys.exit(result.returncode)


def cmd_transcribe(args):
    """仅转写：视频文件 → 文字"""
    video = args.video
    output_dir = os.path.abspath(args.output) if args.output else os.path.dirname(video)
    model = args.model or "medium"

    if not os.path.exists(video):
        print(f"❌ 视频文件不存在: {video}", file=sys.stderr)
        sys.exit(1)

    print(f"🎤 开始转写: {os.path.basename(video)}")
    print(f"   模型: {model}")
    print(f"   语言: {args.language or 'auto'}")
    print(f"   输出目录: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    whisper_cmd = [
        "uvx", "--from", "openai-whisper", "whisper",
        video,
        "--model", model,
        "--output_dir", output_dir,
    ]
    if args.language:
        whisper_cmd.extend(["--language", args.language])

    try:
        subprocess.run(whisper_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 转写失败 (退出码 {e.returncode})", file=sys.stderr)
        # 常见错误提示
        if "SHA256 checksum" in str(e):
            print("  提示: 模型文件校验失败, 请删除缓存后重试:", file=sys.stderr)
            print(f"    rm -f ~/.cache/whisper/{model}.pt", file=sys.stderr)
        sys.exit(1)

    # 列出输出文件
    base = os.path.splitext(os.path.basename(video))[0]
    print(f"\n✅ 转写完成! 输出文件:")
    for ext in ["txt", "srt", "vtt", "tsv", "json"]:
        fp = os.path.join(output_dir, f"{base}.{ext}")
        if os.path.exists(fp):
            size = os.path.getsize(fp)
            print(f"   📄 {base}.{ext} ({size/1024:.0f} KB)")

    return os.path.join(output_dir, f"{base}.txt")


def cmd_pipeline(args):
    """完整流水线：下载 → 转写 → 报告"""
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    # 步骤1: 下载
    print("=" * 50)
    print("步骤 1/3: 下载视频")
    print("=" * 50)

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
        print("❌ 下载失败，终止流水线", file=sys.stderr)
        sys.exit(1)

    # 查找下载的视频
    video = find_video_file(output_dir)
    if not video:
        # 可能藏在子目录中（合集多分类）
        for root, dirs, files in os.walk(output_dir):
            for f in files:
                if f.endswith(".mp4"):
                    video = os.path.join(root, f)
                    break
            if video:
                break

    if not video:
        print("❌ 找不到已下载的视频文件", file=sys.stderr)
        sys.exit(1)

    # 步骤2: 转写
    print("\n" + "=" * 50)
    print("步骤 2/3: 语音转写")
    print("=" * 50)

    # 把转写结果放在 video 同目录
    model = args.model or "medium"
    txt_path = cmd_transcribe(argparse.Namespace(
        video=video,
        output=os.path.dirname(video),
        model=model,
        language=args.language,
    ))

    # 步骤3: 提示后续总结
    print("\n" + "=" * 50)
    print("步骤 3/3: 自动总结")
    print("=" * 50)
    print(f"\n转写文本已保存至: {txt_path}")
    print("\n现在将基于转写文本为您生成内容总结...")

    # 读取转写文本
    if txt_path and os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"\n转写字数: {len(text)} 字")
        print(f"转写时长: {len(text)/4/60:.0f} 分钟 (估算阅读时间)")

    print(f"\n✅ 流水线完成！转写文本: {txt_path}")


def main():
    parser = argparse.ArgumentParser(description="B站视频 下载→转写→总结 流水线")
    sub = parser.add_subparsers(dest="command")

    # info 子命令
    p_info = sub.add_parser("info", help="查看视频信息")
    p_info.add_argument("url", help="B站视频 URL")

    # transcribe 子命令
    p_tr = sub.add_parser("transcribe", help="转写已下载的视频文件")
    p_tr.add_argument("video", help="视频文件路径")
    p_tr.add_argument("-o", "--output", help="输出目录（默认视频所在目录）")
    p_tr.add_argument("--model", default="medium", help="whisper 模型 (tiny/base/small/medium/large-v3)")
    p_tr.add_argument("--language", default="zh", help="语言代码 (zh/en/ja, 默认 zh，空=auto)")

    # pipeline 子命令
    p_pl = sub.add_parser("pipeline", help="完整流水线：下载 → 转写 → 输出文字")
    p_pl.add_argument("url", help="B站视频 URL")
    p_pl.add_argument("-o", "--output", required=True, help="输出目录")
    p_pl.add_argument("-b", "--browser", default="", help="浏览器名称 (chrome/edge/firefox)")
    p_pl.add_argument("-c", "--collection", action="store_true", help="下载整个合集")
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
