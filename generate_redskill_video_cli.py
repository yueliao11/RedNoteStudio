"""
Generate the Chinese REDSkill submission video using edge-tts CLI.
The CLI path is more reliable for long Chinese narrations than the async API.
"""

import subprocess
import sys
import time
from pathlib import Path

# Add local backend to path.
BACKEND = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BACKEND))

from app import config
from app.core import renderer, subtitles, video_builder
from app.parsers.pptx_parser import parse_pptx
from app.utils import hash as hash_util
from app.utils import storage as storage_util


class FakeRequest:
    class URL:
        scheme = "http"
        netloc = "localhost:8000"

    url = URL()


def _base_url(request) -> str:
    return f"{request.url.scheme}://{request.url.netloc}"


def _get_audio_duration(path: Path) -> float:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def _synthesize_with_cli(narrations: list[str], voice: str, work_dir: Path) -> list[dict]:
    selected_voice = {
        "male_zh": "zh-CN-YunxiNeural",
        "female_zh": "zh-CN-XiaoxiaoNeural",
        "male_en": "en-US-GuyNeural",
        "female_en": "en-US-JennyNeural",
    }.get(voice, "zh-CN-XiaoxiaoNeural")

    audio_files = []
    for idx, text in enumerate(narrations):
        out_path = work_dir / f"slide_{idx:03d}.mp3"
        print(f"[tts] slide {idx}: synthesizing via edge-tts CLI...")
        try:
            subprocess.run(
                [
                    "edge-tts",
                    "-t", text,
                    "-v", selected_voice,
                    "--write-media", str(out_path),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=90,
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            print(f"[tts] edge-tts CLI error: {exc.stderr.decode('utf-8', errors='ignore')}")
            raise RuntimeError(f"TTS failed for slide {idx}") from exc

        duration = _get_audio_duration(out_path)
        audio_files.append({"path": out_path, "duration_seconds": duration})
        print(f"[tts] slide {idx}: {out_path.stat().st_size} bytes, {duration:.2f}s")
        time.sleep(0.8)
    return audio_files


def main():
    example_dir = Path(__file__).resolve().parent
    pptx_path = example_dir / "redskill-pitchflow-deck.pptx"
    script_path = example_dir / "redskill_script_zh.txt"

    if not pptx_path.exists():
        print("Generating REDSkill deck first...")
        subprocess.run([sys.executable, str(example_dir / "generate_redskill_ppt.py")], check=True)

    custom_script = script_path.read_text(encoding="utf-8").strip()
    narrations = [s.strip() for s in custom_script.split("---") if s.strip()]
    print(f"Using custom script with {len(narrations)} segments.")

    from uuid import uuid4
    job_id = str(uuid4())
    work_dir = config.OUTPUTS_DIR / job_id
    work_dir.mkdir(parents=True, exist_ok=True)
    input_path = work_dir / "input.pptx"
    input_path.write_bytes(pptx_path.read_bytes())

    slides = parse_pptx(input_path)
    if len(narrations) != len(slides):
        raise ValueError(f"Script segments ({len(narrations)}) must match slide count ({len(slides)})")

    voice = "female_zh"
    language = "zh"
    video_style = "product_demo"
    include_subtitles = True

    # Render slide images
    image_paths = []
    for idx, slide in enumerate(slides):
        img_path = work_dir / f"slide_{idx:03d}.png"
        renderer.render_slide(
            slide, idx, len(slides),
            style=video_style,
            language=language,
            watermark=False,
            caption=narrations[idx] if include_subtitles else None,
            output_path=img_path,
        )
        image_paths.append(img_path)

    # Synthesize audio via CLI
    audio_infos = _synthesize_with_cli(narrations, voice, work_dir)
    audio_paths = [info["path"] for info in audio_infos]
    durations = [info["duration_seconds"] for info in audio_infos]

    # Subtitles
    srt_path = work_dir / "output.srt"
    subtitles.build_srt(narrations, durations, srt_path)

    # Cover
    cover_path = work_dir / "cover.png"
    first_title = slides[0].get("title") or "Agent Generated Video"
    renderer.render_cover(
        first_title,
        subtitle="小红书 AI 视频笔记生成 Skill",
        style=video_style,
        language=language,
        output_path=cover_path,
    )

    # Video
    video_path = work_dir / "output.mp4"
    video_builder.build_video(image_paths, audio_paths, durations, video_path)

    # Metadata
    content_hash = hash_util.sha256_file(video_path)
    metadata = {
        "title": first_title,
        "language": language,
        "voice": voice,
        "style": video_style,
        "slides_count": len(slides),
        "duration_seconds": round(sum(durations), 2),
        "content_hash": content_hash,
        "files": {
            "video": "output.mp4",
            "subtitle": "output.srt",
            "cover": "cover.png",
            "metadata": "metadata.json",
        },
        "narrations": narrations,
    }
    storage_util.save_metadata(work_dir, metadata)

    base = _base_url(FakeRequest())
    result = {
        "status": "success",
        "job_id": job_id,
        "video_url": f"{base}/outputs/{job_id}/output.mp4",
        "subtitle_url": f"{base}/outputs/{job_id}/output.srt",
        "cover_image_url": f"{base}/outputs/{job_id}/cover.png",
        "metadata_url": f"{base}/outputs/{job_id}/metadata.json",
        "duration_seconds": metadata["duration_seconds"],
        "slides_count": len(slides),
        "content_hash": content_hash,
        "metadata": {
            "title": first_title,
            "language": language,
            "voice": voice,
            "style": video_style,
        },
    }

    # Copy artifacts into /redskill for submission convenience.
    for name in ["output.mp4", "output.srt", "cover.png", "metadata.json"]:
        src = work_dir / name
        if src.exists():
            dst = example_dir / f"redskill-output-{name}"
            dst.write_bytes(src.read_bytes())
            print(f"Copied to {dst}")

    print("\nREDSkill submission video generation complete:")
    print(f"  Job ID: {job_id}")
    print(f"  Video:  {result['video_url']}")
    print(f"  Hash:   {result['content_hash']}")


if __name__ == "__main__":
    main()
