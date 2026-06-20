# RedNote Studio / 红书笔记工坊

## 基本信息

- **Skill 名称**：RedNote Studio（红书笔记工坊）
- **版本**：1.0.0
- **作者**：yueliao11
- **GitHub**：https://github.com/yueliao11/RedNoteStudio
- **标签**：#AI视频 #PPT转视频 #小红书运营 #内容创作 #AIGC #AgentSkill
- **适用平台**：macOS / Linux / Windows（WSL）
- **所需权限**：本地文件读取、命令行执行、网络访问（仅 edge-tts 语音合成）

## 一句话介绍

把 PPT、讲义、产品资料一键转成带中文语音讲解的小红书视频笔记。

## 技能描述

RedNote Studio 是一个可复用的 AI Agent Skill，专为小红书等内容平台设计。它能够：

1. 读取 PPTX 文件，自动提取每页标题和核心要点；
2. 自动生成自然中文讲稿，支持自定义脚本；
3. 调用 Microsoft Azure 神经语音（edge-tts）合成中文女声/男声配音；
4. 通过 ffmpeg 输出 1080P MP4，自带同步字幕；
5. 同时输出封面图、SRT 字幕、结构化 metadata 和内容指纹。

相比传统剪辑软件，RedNote Studio 是 API 化的 Agent Skill，可嵌入任何内容工作流，支持批量生产。

## 使用场景

- **知识博主**：把课件、大纲批量转成口播短视频；
- **品牌种草**：产品资料一键生成带货解说视频；
- **教育机构**：把讲义变成学生可反复观看的短视频；
- **矩阵号运营**：统一风格、批量生成视频笔记。

## 安装与运行

### 前置依赖

- Python 3.10+
- ffmpeg / ffprobe
- LibreOffice（用于真实导出 PPT 页面，可选）

### macOS 一键安装

```bash
# 克隆仓库
git clone https://github.com/yueliao11/RedNoteStudio.git
cd RedNoteStudio

# 创建虚拟环境并安装依赖
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 安装 LibreOffice（用于导出真实 PPT 页面）
brew install --cask libreoffice
```

### 快速使用

```bash
# 方式一：用真实 PPT 页面作为背景生成讲解视频
python generate_real_ppt_narrated_video.py

# 方式二：生成参赛 Demo（含 PPT + 视频 + 海报）
python generate_redskill_ppt.py
python generate_redskill_video_cli.py
python generate_redskill_poster.py

# 方式三：启动 API 服务
python backend/app/main.py
```

### API 调用

```bash
curl -X POST http://localhost:8000/skill/generate \
  -F "pptx_file=@RedNote Studio - 小红书 AI 视频笔记生成 Skill.pptx" \
  -F "video_style=product_demo" \
  -F "voice=female_zh" \
  -F "language=zh" \
  -F "include_subtitles=true"
```

## 文件结构

```
RedNoteStudio/
├── SKILL.md                              # 本文件
├── README.md                             # 项目说明
├── requirements.txt                      # Python 依赖
├── backend/app/                          # FastAPI Skill 核心
│   ├── main.py
│   ├── config.py
│   ├── parsers/pptx_parser.py
│   └── core/
│       ├── narration.py
│       ├── tts.py
│       ├── renderer.py
│       ├── video_builder.py
│       └── subtitles.py
├── generate_real_ppt_narrated_video.py   # 真实 PPT 背景 + 语音讲解
├── generate_existing_ppt_demo.py         # 已有 PPT 讲解 Demo
├── generate_full_process_demo.py         # 完整流程 Demo
├── generate_redskill_ppt.py              # 生成参赛 PPT
├── generate_redskill_video_cli.py        # 生成参赛视频
├── generate_redskill_poster.py           # 生成小红书封面海报
├── redskill_script_zh.txt                # 默认中文讲稿
├── demo_script_zh.txt                    # 已有 PPT 讲解稿
├── RedNote Studio - 小红书 AI 视频笔记生成 Skill.pptx
└── rednote-real-ppt-narrated-output.mp4  # 示例输出视频
```

## 输出示例

运行 `python generate_real_ppt_narrated_video.py` 后，会得到：

- `rednote-real-ppt-narrated-output.mp4` — 1080P 中文语音讲解视频
- `rednote-real-ppt-narrated-output.srt` — 同步中文字幕

## 权限与用途说明

- **文件读取**：仅读取用户提供的 PPTX 文件和自定义脚本 TXT；
- **命令行执行**：调用 `soffice`、`edge-tts`、`ffmpeg` 等外部工具生成视频；
- **网络访问**：仅用于 edge-tts 调用 Microsoft Azure 语音合成服务；
- **输出文件**：生成视频、字幕、封面图保存在本地 `data/outputs/` 目录；
- **无隐藏行为**：所有代码开源在 GitHub，不收集用户数据，不上传文件到远程服务器。

## 代码透明

本 Skill 全部代码开源：https://github.com/yueliao11/RedNoteStudio

核心依赖：
- FastAPI / uvicorn
- python-pptx
- Pillow
- edge-tts
- ffmpeg

## 参赛宣言

RedNote Studio：让每一份内容资料，都能被听见、被看见、被传播。
