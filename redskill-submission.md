# RedNote Studio — 小红书 REDSkill 大赏参赛材料

> 活动：小红书科技 REDSkill 大赏（6 月 8 日 – 7 月 20 日）
> 参赛项目：RedNote Studio — 小红书 AI 视频笔记生成 Skill

---

## 1. 项目标题

**RedNote Studio：小红书 AI 视频笔记生成 Skill**

## 2. 一句话介绍

RedNote Studio 是一个可复用的 AI Agent Skill，能把 PPT、讲义、产品资料一键转成带中文语音讲解的小红书视频笔记。

## 3. 参赛视频

- **文件**：`redskill/redskill-output-output.mp4`
- **时长**：约 147 秒
- **分辨率**：1920 × 1080
- **语音**：中文女声（Microsoft Azure Neural）
- **内容**：8 页小红书主题 PPT + 高质量手写中文讲稿
- **配套字幕**：`redskill/redskill-output-output.srt`

## 4. 封面 / 海报

- **文件**：`redskill/redskill-poster.png`
- **尺寸**：1080 × 1440（小红书 3:4 封面比例）

## 5. 核心亮点

1. **端到端闭环**：上传 PPTX → 提取文本 → 生成中文讲稿 → 语音合成 → 视频合成 → 输出字幕/封面/metadata。
2. **中文优先**：默认中文女声，支持中文男声，讲稿自然、适合口播。
3. **小红书优化**：输出 1080P 视频 + 1080×1440 封面海报 + SRT 字幕，可直接二次剪辑发布。
4. **Agent 原生**：提供 FastAPI Skill 接口，可嵌入任何内容工作流，支持批量生产。
5. **真实可运行**：无需 LLM Key 也能通过 `custom_script` 模式生成高质量视频，评委可本地一键复现。

## 6. 技术栈

- **后端**：Python · FastAPI · ffmpeg · Pillow · edge-tts · python-pptx
- **前端**：HTML · CSS · JavaScript
- **部署**：本地一键脚本 + 可扩展为云端 API

## 7. 本地复现方式

```bash
# 1. 进入项目
cd pharos-pitchflow

# 2. 激活环境
source backend/.venv/bin/activate

# 3. 生成参赛 PPT、讲解视频与海报
python redskill/generate_redskill_ppt.py
python redskill/generate_redskill_video_cli.py
python redskill/generate_redskill_poster.py

# 输出文件在 redskill/ 目录：
#   redskill-pitchflow-deck.pptx
#   redskill-output-output.mp4
#   redskill-output-output.srt
#   redskill-output-cover.png
#   redskill-poster.png
```

## 8. 差异化

| 传统剪辑软件 | RedNote Studio Skill |
|---|---|
| 人工写稿、配音、剪辑 | Agent 自动解析 PPT 并生成视频 |
| 学习成本高 | 上传 PPTX 即可 |
| 单机文件 | API 化，可嵌入任何工作流 |
| 难以批量 | 可脚本化批量生产 |

## 9. 未来规划

- 从 Skill 升级为完整 **内容生产 Agent**
- 接收选题、链接或文档，自动生成 PPT 脚本
- 生成多音色、多风格视频
- 自动导出封面、字幕和发布文案
- 对接小红书、抖音、B 站等内容平台

## 10. 小红书投稿文案（可直接发布）

```text
🎬 我把 PPT 丢给 AI，它居然自动讲成了小红书视频？

参赛 #REDSkill大赏，给大家介绍 RedNote Studio：
一个让 AI Agent 把 PPT 自动转成「中文语音视频笔记」的 Skill。

✅ 上传 PPTX → 自动生成讲稿 + 中文配音 + 字幕
✅ 输出 1080P 视频 + 小红书封面海报 + SRT 字幕
✅ 无需剪辑基础，资料直接变视频
✅ API 化设计，可批量生产矩阵号内容

知识博主、品牌种草、教育机构都能用 🤖🎙️

#REDSkill大赏 #小红书科技 #AIAgent #PPT转视频 #AIGC #视频笔记 #内容创作 #RedNote Studio
```

---

**GitHub 仓库**：https://github.com/yueliao11/pharos-pitchflow
