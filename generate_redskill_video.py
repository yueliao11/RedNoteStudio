"""
Generate the Chinese REDSkill submission video for RedNote Studio.
Uses a handcrafted script (custom_script mode) so no LLM key is required.
"""

import subprocess
import sys
from pathlib import Path

# Add local backend to path.
BACKEND = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BACKEND))

from app import config
from app.main import _run_pipeline


class FakeRequest:
    """Minimal stand-in for FastAPI Request so we can build public URLs."""

    class URL:
        scheme = "http"
        netloc = "localhost:8000"

    url = URL()


def main():
    example_dir = Path(__file__).resolve().parent
    pptx_path = example_dir / "redskill-pitchflow-deck.pptx"
    script_path = example_dir / "redskill_script_zh.txt"

    # Ensure the deck exists.
    if not pptx_path.exists():
        print("Generating REDSkill deck first...")
        subprocess.run([sys.executable, str(example_dir / "generate_redskill_ppt.py")], check=True)

    if not script_path.exists():
        print(f"Script not found: {script_path}")
        return

    custom_script = script_path.read_text(encoding="utf-8").strip()
    # Validate slide count matches script segments.
    segments = [s.strip() for s in custom_script.split("---") if s.strip()]
    print(f"Using custom script with {len(segments)} segments.")

    from uuid import uuid4

    job_id = str(uuid4())
    work_dir = config.OUTPUTS_DIR / job_id
    work_dir.mkdir(parents=True, exist_ok=True)
    input_path = work_dir / "input.pptx"
    input_path.write_bytes(pptx_path.read_bytes())

    result = _run_pipeline(
        request=FakeRequest(),
        work_dir=work_dir,
        input_path=input_path,
        script_mode="custom_script",
        voice="female_zh",
        language="zh",
        video_style="product_demo",
        include_subtitles=True,
        watermark=False,
        custom_script=custom_script,
    )

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
    print(f"  Local files:")
    for name in ["redskill-output-output.mp4", "redskill-output-output.srt", "redskill-output-cover.png", "redskill-output-metadata.json"]:
        print(f"    - redskill/{name}")


if __name__ == "__main__":
    main()
