"""
Generate a Xiaohongshu / REDSkill Awards style poster for RedNote Studio.
Output: 1080x1440 PNG, content-creator friendly aesthetic.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _load_font(size: int, lang: str = "zh") -> ImageFont.FreeTypeFont:
    candidates = []
    if lang == "zh":
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
        ]
    else:
        candidates = [
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _draw_grid(draw: ImageDraw.ImageDraw, w: int, h: int, step: int = 60):
    """Subtle warm grid on light background."""
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=(245, 240, 235), width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=(245, 240, 235), width=1)


def _gradient_background(width: int, height: int) -> Image.Image:
    top = (255, 250, 245)
    bottom = (255, 240, 235)
    img = Image.new("RGB", (width, height), top)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / height
        r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
        g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
        b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img


def _rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def main():
    W, H = 1080, 1440
    img = _gradient_background(W, H)
    draw = ImageDraw.Draw(img)
    _draw_grid(draw, W, H, step=60)

    # Fonts
    tag_font = _load_font(32)
    title_font = _load_font(130)
    subtitle_font = _load_font(42)
    body_font = _load_font(32)
    small_font = _load_font(26)
    slogan_font = _load_font(30)

    # Colors
    red = (255, 36, 66)
    dark = (45, 45, 55)
    muted = (100, 100, 115)

    # Top "小红书 科技" tag
    tag_text = "小红书 科技"
    tag_w, tag_h = 220, 60
    tag_x = (W - tag_w) // 2
    tag_y = 80
    _rounded_rect(draw, (tag_x, tag_y, tag_x + tag_w, tag_y + tag_h), 30, fill=red)
    bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((tag_x + (tag_w - tw) // 2, tag_y + (tag_h - th) // 2 - 6), tag_text, font=tag_font, fill=(255, 255, 255))

    # Main title
    title = "RedNote Studio"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 190), title, font=title_font, fill=dark)

    # Subtitle
    subtitle = "小红书 AI 视频笔记生成 Skill"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 360), subtitle, font=subtitle_font, fill=muted)

    # Pipeline diagram
    box_w, box_h = 180, 72
    gap = 24
    start_x = (W - (4 * box_w + 3 * gap)) // 2
    y_box = 480
    steps = ["PPT", "讲稿", "语音", "视频"]
    for i, step in enumerate(steps):
        x = start_x + i * (box_w + gap)
        _rounded_rect(draw, (x, y_box, x + box_w, y_box + box_h), 14, fill=(255, 255, 255), outline=red, width=2)
        bbox = draw.textbbox((0, 0), step, font=body_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x + (box_w - tw) // 2, y_box + (box_h - th) // 2 - 6), step, font=body_font, fill=dark)
        if i < len(steps) - 1:
            ax = x + box_w + 4
            ay = y_box + box_h // 2
            draw.polygon([(ax, ay - 8), (ax + 18, ay), (ax, ay + 8)], fill=red)

    # Feature bullets
    features = [
        "上传 PPTX → 自动生成中文讲稿与配音",
        "输出 1080P 视频 + SRT 字幕 + 封面图",
        "自动生成 1080×1440 小红书封面海报",
        "API 化设计，支持批量内容生产",
    ]
    y_feat = 620
    for feat in features:
        draw.text((100, y_feat), f"• {feat}", font=body_font, fill=dark)
        y_feat += 60

    # Use cases
    cases_title = "适合谁用"
    draw.text((100, y_feat + 20), cases_title, font=body_font, fill=dark)
    cases = "知识博主  ·  品牌种草  ·  教育机构  ·  矩阵号运营"
    bbox = draw.textbbox((0, 0), cases, font=small_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y_feat + 80), cases, font=small_font, fill=muted)

    # Slogan
    slogan = "让每一份内容资料，都能被听见、被看见、被传播"
    bbox = draw.textbbox((0, 0), slogan, font=slogan_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 1180), slogan, font=slogan_font, fill=red)

    # Bottom award line
    award = "REDSkill 大赏 参赛项目"
    bbox = draw.textbbox((0, 0), award, font=small_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 1300), award, font=small_font, fill=muted)

    # Decorative circles
    draw.ellipse([(W - 200, H - 320), (W - 40, H - 160)], outline=(255, 220, 220), width=2)
    draw.ellipse([(40, 180), (140, 280)], outline=(255, 220, 220), width=2)

    out = Path(__file__).with_name("redskill-poster.png")
    img.save(out, "PNG")
    print(f"Created REDSkill poster: {out}")


if __name__ == "__main__":
    main()
