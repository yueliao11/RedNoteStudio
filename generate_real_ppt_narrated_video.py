"""
Generate a narrated video using the REAL original PPTX slides as background.
Each slide is shown for the duration of its corresponding Chinese narration.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Add local backend to path.
BACKEND = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BACKEND))

from app.core import subtitles


PPT_DIR = Path(__file__).resolve().parent


def _check_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"Required tool not found: {name}. Please install it.")
    return path


def _export_pptx_to_pngs(pptx_path: Path, output_dir: Path) -> list[Path]:
    """Export each PPTX slide to a high-resolution PNG using LibreOffice + pdftoppm."""
    _check_tool("soffice")
    _check_tool("pdftoppm")

    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_dir),
            str(pptx_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    pdf_files = list(output_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError("LibreOffice did not produce a PDF.")
    pdf_file = pdf_files[0]

    pages_prefix = output_dir / "page"
    subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-r", "300",
            str(pdf_file),
            str(pages_prefix),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    pages = sorted(output_dir.glob("page-*.png"))
    if not pages:
        raise FileNotFoundError("pdftoppm did not produce PNG pages.")
    return pages


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
    }.get(voice, "zh-CN-XiaoxiaoNeural")

    audio_files = []
    for idx, text in enumerate(narrations):
        out_path = work_dir / f"slide_{idx:03d}.mp3"
        print(f"[tts] slide {idx}: synthesizing via edge-tts CLI...")
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
        duration = _get_audio_duration(out_path)
        audio_files.append({"path": out_path, "duration_seconds": duration})
        print(f"[tts] slide {idx}: {out_path.stat().st_size} bytes, {duration:.2f}s")
        if idx < len(narrations) - 1:
            subprocess.run(["sleep", "0.8"], check=True)
    return audio_files


def _build_video(slide_images: list[Path], audio_files: list[Path], durations: list[float], output_path: Path, work_dir: Path) -> Path:
    video_only = work_dir / "video_only_real.mp4"
    audio_list = work_dir / "audio_list_real.txt"
    audio_only = work_dir / "audio_only_real.aac"

    safe_durations = [max(2.0, d) for d in durations]

    # 1. Build silent video from real slide images.
    inputs: list[str] = []
    for img, duration in zip(slide_images, safe_durations):
        inputs.extend(["-loop", "1", "-t", str(duration), "-i", str(img)])

    filter_parts: list[str] = []
    for idx, _duration in enumerate(safe_durations):
        filter_parts.append(
            f"[{idx}:v]scale=1920:1080:force_original_aspect_ratio=decrease,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,"
            f"fps=30,format=yuv420p,setpts=PTS-STARTPTS[v{idx}];"
        )
    concat_inputs = "".join(f"[v{idx}]" for idx in range(len(slide_images)))
    filter_parts.append(f"{concat_inputs}concat=n={len(slide_images)}:v=1:a=0[vv]")

    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        *inputs,
        "-filter_complex",
        "".join(filter_parts),
        "-map", "[vv]",
        "-an",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        str(video_only),
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # 2. Build concatenated audio.
    audio_list.write_text(
        "\n".join(f"file '{a.resolve()}'" for a in audio_files), encoding="utf-8"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-nostdin",
            "-f", "concat",
            "-safe", "0",
            "-i", str(audio_list),
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "48000",
            str(audio_only),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    # 3. Merge.
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-nostdin",
            "-i", str(video_only),
            "-i", str(audio_only),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "48000",
            "-shortest",
            str(output_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return output_path


def main():
    pptx_path = PPT_DIR / "RedNote Studio - 小红书 AI 视频笔记生成 Skill.pptx"
    script_path = PPT_DIR / "demo_script_zh.txt"

    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    custom_script = script_path.read_text(encoding="utf-8").strip()
    narrations = [s.strip() for s in custom_script.split("---") if s.strip()]
    print(f"Using custom script with {len(narrations)} segments.")

    temp_dir = Path(tempfile.mkdtemp(prefix="rednote_real_ppt_"))
    final_output = PPT_DIR / "rednote-real-ppt-narrated-output.mp4"

    try:
        print("[1/3] Exporting original PPTX slides to real PNGs via LibreOffice...")
        slide_images = _export_pptx_to_pngs(pptx_path, temp_dir / "slides")
        print(f"      Exported {len(slide_images)} slides.")

        if len(narrations) != len(slide_images):
            raise ValueError(
                f"Narrations ({len(narrations)}) must match slides ({len(slide_images)})."
            )

        print("[2/3] Synthesizing Chinese narration audio...")
        audio_infos = _synthesize_with_cli(narrations, "female_zh", temp_dir)
        audio_paths = [info["path"] for info in audio_infos]
        durations = [info["duration_seconds"] for info in audio_infos]

        print("[3/3] Building video with real PPT slides as background...")
        _build_video(slide_images, audio_paths, durations, final_output, temp_dir)

        # Generate SRT subtitle.
        srt_path = PPT_DIR / "rednote-real-ppt-narrated-output.srt"
        subtitles.build_srt(narrations, durations, srt_path)

        print(f"\nReal-PPT narrated video saved to: {final_output}")
        print(f"Subtitle saved to: {srt_path}")
        print(f"Total duration: {sum(durations):.2f}s")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
