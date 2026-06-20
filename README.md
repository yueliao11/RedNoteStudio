# RedNote Studio / 红书笔记工坊

> **一个 AI Agent Skill，把 PPT、讲义、产品资料一键转成带中文语音讲解的小红书视频笔记。**

RedNote Studio（红书笔记工坊）专为小红书等内容平台设计：

- 上传 PPTX，Agent 自动提取标题与要点；
- 生成自然中文讲稿，支持自定义脚本；
- 调用 Microsoft Azure 神经语音合成中文配音；
- ffmpeg 输出 1080P MP4，自带同步字幕；
- 同时输出封面图、SRT 字幕、结构化 metadata 和内容指纹。

---

## 快速开始

### 1. 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

> 需要系统已安装 `ffmpeg` 和 `ffprobe`。

### 2. 一键生成参赛 Demo

```bash
source .venv/bin/activate
python generate_redskill_ppt.py
python generate_redskill_video_cli.py
python generate_redskill_poster.py
```

输出：

- `redskill-output-output.mp4` — 带中文语音讲解的视频
- `redskill-output-output.srt` — 同步中文字幕
- `redskill-output-cover.png` — 视频封面
- `redskill-poster.png` — 小红书 3:4 封面海报

### 3. 用 Skill 讲解已有 PPT

仓库里已有一份参赛 PPT `RedNote Studio - 小红书 AI 视频笔记生成 Skill.pptx`，可以用 Skill 自己讲解自己：

```bash
source .venv/bin/activate
python generate_existing_ppt_demo.py
```

输出：

- `rednote-existing-demo-output.mp4` — 约 3 分 24 秒中文语音讲解视频
- `rednote-existing-demo-output.srt` — 同步字幕
- `rednote-existing-demo-cover.png` — 视频封面

### 4. 真实 PPT 页面 + 中文语音讲解视频

直接用原始 PPT 页面作为背景，一页一页配上中文语音讲解：

```bash
source .venv/bin/activate
python generate_real_ppt_narrated_video.py
```

> 需要系统已安装 `soffice`（LibreOffice）和 `pdftoppm`。
> macOS 可通过 `brew install --cask libreoffice` 安装。

输出：

- `rednote-real-ppt-narrated-output.mp4` — 约 3 分 24 秒讲解视频
- `rednote-real-ppt-narrated-output.srt` — 同步中文字幕

### 5. 完整流程 Demo：先看静态 PPT，再看 Skill 转换，最后看生成结果

```bash
source .venv/bin/activate
python generate_full_process_demo.py
```

输出：

- `rednote-full-process-demo-output.mp4` — 约 3 分 52 秒完整流程视频
  - 前 24 秒：用 LibreOffice 真实导出并静态展示原始 PPT 的 8 页内容
  - 中间 4 秒：过渡页说明正在使用 RedNote Studio Skill 转换
  - 后 3 分 24 秒：最终生成的中文语音讲解视频

### 5. 启动 API 服务

```bash
cd backend
source ../.venv/bin/activate
python -m app.main
```

服务默认运行在 `http://localhost:8000`。

### 4. 调用 Skill

```bash
curl -X POST http://localhost:8000/skill/generate \
  -F "pptx_file=@redskill-pitchflow-deck.pptx" \
  -F "video_style=product_demo" \
  -F "voice=female_zh" \
  -F "language=zh" \
  -F "include_subtitles=true"
```

---

## 项目结构

```
redskill/
├── README.md
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── parsers/pptx_parser.py
│       └── core/
│           ├── narration.py
│           ├── tts.py
│           ├── renderer.py
│           ├── video_builder.py
│           └── subtitles.py
├── generate_redskill_ppt.py
├── generate_redskill_video.py
├── generate_redskill_video_cli.py
├── generate_existing_ppt_demo.py
├── generate_full_process_demo.py
├── generate_real_ppt_narrated_video.py
├── generate_redskill_poster.py
├── redskill_script_zh.txt
├── demo_script_zh.txt
├── RedNote Studio - 小红书 AI 视频笔记生成 Skill.pptx
├── redskill-pitchflow-deck.pptx
├── redskill-output-output.mp4
├── redskill-output-output.srt
├── redskill-output-cover.png
├── redskill-poster.png
├── rednote-existing-demo-output.mp4
├── rednote-existing-demo-output.srt
├── rednote-existing-demo-cover.png
├── rednote-full-process-demo-output.mp4
└── redskill-submission.md
```

---

## REDSkill 大赏参赛材料

- **参赛视频**：`redskill-output-output.mp4`
- **真实 PPT 语音讲解视频**：`rednote-real-ppt-narrated-output.mp4`
- **已有 PPT 讲解 Demo**：`rednote-existing-demo-output.mp4`
- **完整流程 Demo（静态 PPT + Skill 转换 + 生成结果）**：`rednote-full-process-demo-output.mp4`
- **参赛 PPT**：`redskill-pitchflow-deck.pptx`
- **小红书封面**：`redskill-poster.png`
- **投稿文案**：`redskill-submission.md`

---

## License

MIT — built for the REDSkill Awards.
