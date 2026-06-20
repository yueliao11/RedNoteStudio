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

### 3. 启动 API 服务

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
├── generate_redskill_poster.py
├── redskill_script_zh.txt
├── redskill-pitchflow-deck.pptx
├── redskill-output-output.mp4
├── redskill-output-output.srt
├── redskill-output-cover.png
├── redskill-poster.png
└── redskill-submission.md
```

---

## REDSkill 大赏参赛材料

- **参赛视频**：`redskill-output-output.mp4`
- **参赛 PPT**：`redskill-pitchflow-deck.pptx`
- **小红书封面**：`redskill-poster.png`
- **投稿文案**：`redskill-submission.md`

---

## License

MIT — built for the REDSkill Awards.
