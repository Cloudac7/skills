---
name: video-to-summary
description: "短视频平台链接（抖音/小红书/B站/YouTube）或本地视频/音频文件 → 字幕转写 + AI 内容总结。当用户要求下载并总结视频、将视频转文字、提取视频字幕时触发。支持所有常见短视频分享链接和本地文件。典型场景：'把这个B站视频转成文字'、'下载并总结这个抖音'、'帮我整理这个YouTube视频的要点'、'转写这个本地视频文件'。"
---

# 视频 → 字幕转写 → AI 总结

将短视频平台链接或本地视频/音频文件转为字幕文字并生成 AI 总结。

**支持平台：** 抖音/TikTok、小红书、B站、YouTube、本地视频/音频文件

**核心流程：**
- **在线视频：** 获取视频信息 → 下载视频 → 提取音频 → 选择 ASR 后端 → 转写字幕 → AI 总结
- **本地文件：** 提取音频（如需）→ 选择 ASR 后端 → 转写 → AI 总结
- **YouTube（特殊）：** 优先用 yt-dlp 抓取手动字幕或自动字幕，字幕不可用时才回退到 ASR

## 依赖

| 依赖 | 用途 | 必需 |
|------|------|------|
| `yt-dlp` | B站/YouTube 下载、YouTube 字幕抓取 | B站/YouTube 必需 |
| `ffmpeg` | 从视频提取音频 | 非音频文件时必需 |
| `uvx` | 运行 openai-whisper / faster-whisper（自动隔离 Python 环境） | 必需 |

### 安装

```bash
# 基础依赖
pip install yt-dlp
sudo apt install ffmpeg    # Ubuntu/Debian
brew install ffmpeg        # macOS

# ASR 后端：两个都通过 uvx 运行，无需 pip install
# - openai-whisper:  uvx --from openai-whisper whisper ...
# - faster-whisper:  uvx --with faster-whisper --with ctranslate2 python3 <script>

# Bilibili 下载依赖（如果使用 bilibili-downloader-plus 的脚本）
python3 {SKILL_DIR}/../bilibili-downloader-plus/scripts/ensure_deps.py
```

## 配置

支持通过环境变量或 `.env` 文件配置（按优先级：`{SKILL_DIR}/.env` > 环境变量）：

```env
# --- ASR 后端选择 ---
ASR_BACKEND="whisper"         # whisper (默认, via uvx) 或 faster-whisper

# --- faster-whisper 配置（仅 ASR_BACKEND=faster-whisper 时） ---
FW_MODEL_SIZE="small"         # tiny/base/small/medium/large-v3
FW_DEVICE="auto"              # auto/cpu/cuda
FW_COMPUTE_TYPE=""            # 如 "float16"（GPU 加速）

# --- TikHub Token（抖音/小红书/YouTube 非必需；yt-dlp 有原生支持） ---
TIKHUB_TOKEN=""
```

## 平台识别与工作流

### 步骤 0：判断输入类型

| 输入 | 识别方式 | 策略 |
|------|---------|------|
| `douyin.com`, `v.douyin.com`, `tiktok.com` | URL 域名 | yt-dlp 下载 |
| `xiaohongshu.com`, `xhslink.com` | URL 域名 | yt-dlp 下载 |
| `bilibili.com`, `b23.tv` | URL 域名 | `bilibili-downloader-plus` 脚本（画质/合集逻辑复用） |
| `youtube.com`, `youtu.be` | URL 域名 | yt-dlp 优先抓字幕，失败再下载+ASR |
| 本地 `.mp4`/`.mov`/`.avi` 等 | 文件路径 | 直接进入音频提取 |
| 本地 `.mp3`/`.wav`/`.m4a` 等 | 文件路径 | 跳过音频提取，直接 ASR 转写 |

### 步骤 1：获取视频信息（仅在线视频模式）

```bash
# B站 — 复用 bilibili-downloader-plus 的 info 命令
python3 {SKILL_DIR}/../bilibili-downloader-plus/scripts/bilibili_download.py info "<URL>"

# YouTube — 用 yt-dlp 获取信息
yt-dlp --print title --print duration --print channel "<URL>"

# 抖音/小红书/其他 — 用 yt-dlp 打印基本信息
yt-dlp --print title --print duration --print uploader "<URL>"
```

**合集与画质策略（仅 B站）：**
1. 如果视频属于合集，**主动告知用户**（共 N 集），询问是否下载全部
2. 如果画质 ≤ 480P，询问用户是否授权浏览器 Cookie 获取 1080P+（`--browser chrome/edge/firefox`）
3. 使用 Cookie 前必须征得用户明确同意

### 步骤 2：下载视频（仅在线视频模式）

```bash
# B站 — 复用 bilibili-downloader-plus 脚本
python3 {SKILL_DIR}/../bilibili-downloader-plus/scripts/bilibili_download.py download "<URL>" -o <输出目录>
# 合集：加 --collection
# 浏览器 Cookie：加 --browser chrome

# YouTube — yt-dlp 选择最佳画质
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  --merge-output-format mp4 \
  -o "<输出目录>/%(title)s.%(ext)s" "<URL>"
# YouTube 优先抓字幕（见下文），字幕不存在才下载视频

# 抖音/小红书 — yt-dlp 下载
yt-dlp -f "best" -o "<输出目录>/%(title)s.%(ext)s" "<URL>"
```

**YouTube 字幕优先策略（重要）：**
对于 YouTube 链接，**优先尝试直接抓取字幕**，不下载视频：

```bash
# 抓取字幕（优先中文字幕，fallback 英文）
yt-dlp --skip-download \
  --write-auto-subs --write-subs \
  --sub-langs "zh-Hans,zh-Hant,zh,en" \
  --convert-subs srt \
  -o "/tmp/video_analysis/%(id)s/%(title)s" "<URL>"
```

如果字幕文件存在，直接读取字幕文本，跳过步骤 3-4。如果抓取失败（无字幕），才回退到下载+ASR 流程。

### 步骤 3：提取音频（本地音频文件可跳过）

```bash
ffmpeg -i "<视频文件>" -q:a 0 -map a -y "<输出目录>/audio.mp3"
```

### 步骤 4：ASR 转写

读取 `ASR_BACKEND` 环境变量，默认 `whisper`。

#### 方案 A：ASR_BACKEND=whisper（默认）

使用 `uvx --from openai-whisper whisper`，零安装、自动隔离 Python 环境：

```bash
uvx --from openai-whisper whisper "<视频或音频文件>" \
  --model medium \
  --language zh \
  --output_dir <输出目录>
```

**参数说明：**
- `--model medium` — 推荐。中文精度好，速度可接受（模型 ~1.42GB）
- 快速出稿用 `--model small`（~461MB，快 3-5 倍）
- 中英混杂用 `--model large-v3`（最准但最慢）
- `--language zh` — 中文视频专用；中英混合可省略让 whisper 自动检测

**故障：** checksum mismatch → `rm -f ~/.cache/whisper/<model>.pt` 后重试

#### 方案 B：ASR_BACKEND=faster-whisper（更快，同样 uvx 零安装）

同样通过 `uvx` 运行，无需 `pip install`：

```bash
uvx --with faster-whisper --with ctranslate2 python3 \
  {SKILL_DIR}/scripts/transcribe_faster_whisper.py \
  "<音频文件>" \
  --output_dir <输出目录> \
  --model_size ${FW_MODEL_SIZE:-small} \
  --device ${FW_DEVICE:-auto} \
  --compute_type ${FW_COMPUTE_TYPE}
```

首次运行 uv 会自动安装 `faster-whisper` 和 `ctranslate2` 到临时环境，后续缓存加速。

faster-whisper 相比 openai-whisper 速度快 4x 以上，显存占用低，推荐 GPU 用户使用。

### 步骤 5：读取转写文本

转写完成后会生成以下文件：
- `*.txt` — 纯文本（用于总结）
- `*.srt` / `*.vtt` — 字幕格式（带时间轴）
- `*.json` — 完整 JSON（含 `segments[].text` 和 `segments[].start` 时间戳）

读取 `.txt` 文件作为总结的输入。`.json` 文件在需要精确时间引用时使用。

### 步骤 6：AI 总结

#### 总结结构

始终使用以下模板输出：

## 【视频标题】
平台：B站/抖音/YouTube/...
时长：XX 分钟
UP主/作者：XXX

### 概述
2-3 句话概括核心主题和价值。

### 要点结构
将内容按逻辑分节，每节提炼要点：

**1. 要点一标题**
- 支持细节/例子
- 关键论证

**2. 要点二标题**
- ...

### 关键引用（可选）
2-3 条有代表性原话，标注时间点。
> "原文引用" — 00:01:23

### 总结
一段话提炼核心价值 + 目标受众建议。

#### 生成规则

1. **语言一致** — 中文视频用中文总结，英文视频用英文总结
2. **区分事实与观点** — 明确标注"UP主认为"等立场标记
3. **数字精确** — 视频中提到数字、数据必须准确摘录，**不得编造或近似**
4. **高信息密度** — 避免 AI 套话，用具体内容填充每个要点
5. **独立思考** — 如果视频内容有逻辑问题或值得商榷之处，可以适当指出
6. **目标测试** — 没看过视频的人读完后应能理解核心内容

## 本地文件模式

用户提供本地视频或音频文件路径时的简化流程：

```bash
# 方案 A: openai-whisper（默认）
uvx --from openai-whisper whisper "<本地文件.mp4>" --model medium --language zh --output_dir <目录>

# 方案 B: faster-whisper（更快）
uvx --with faster-whisper --with ctranslate2 python3 \
  {SKILL_DIR}/scripts/transcribe_faster_whisper.py "<本地文件.mp4>" --output_dir <目录>
```

## 设备模式：GPU 加速

如果环境中有 NVIDIA GPU（检查方式：`python3 -c "import torch; print(torch.cuda.is_available())"`）：

```bash
# faster-whisper: 设置 FW_DEVICE=cuda 自动启用 GPU
export FW_DEVICE="cuda"
export FW_COMPUTE_TYPE="float16"
```

## 完整流程示例

用户说"帮我总结这个视频 https://www.bilibili.com/video/BV1uL4y1w71E"

1. 识别平台：B站 → 调用 `bilibili_download.py info` 获取标题/时长/合集信息
2. 告知用户信息，询问合集下载意愿和画质
3. 下载视频
4. 提取音频：`ffmpeg -i video.mp4 -q:a 0 -map a audio.mp3`
5. ASR 转写：`uvx --from openai-whisper whisper audio.mp3 --model medium --language zh`
6. 读取 `.txt` 获取全文
7. 按模板输出总结

用户说"把这个YouTube视频转成文字 https://youtube.com/watch?v=xxx"

1. 识别平台：YouTube → 优先抓字幕
2. `yt-dlp --skip-download --write-auto-subs --sub-langs zh-Hans,zh-Hant,zh,en --convert-subs srt`
3. 如果字幕存在 → 直接读取 `.srt`/`.vtt` 为文字
4. 如果字幕不存在 → 回退下载+ffmpeg+ASR 流程
5. 输出总结

用户说"转写这个本地文件 /path/to/recording.mp4"

1. 判断为本地文件 → 跳过平台识别和下载
2. 提取音频 → ASR 转写
3. 输出文字和总结
