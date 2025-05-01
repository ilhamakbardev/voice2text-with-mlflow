import warnings
import os
import argparse
from pathlib import Path
from utils.recorder import record_audio_dynamic
from utils.transcriber import transcribe_audio

warnings.filterwarnings("ignore")
os.environ["GIT_PYTHON_REFRESH"] = "quiet"


def run_model_cli(model_name="base"):
    print(f"🔧 Selected model: {model_name}")

    audio_dir = Path("audio_recorded")
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_path = audio_dir / "cli_sample.wav"

    record_audio_dynamic(str(audio_path))

    print("🧠 Transcribing...")
    result = transcribe_audio(str(audio_path), model_name=model_name)
    print("\n📜 Transcription Result:")
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Whisper model CLI")
    parser.add_argument("--model", type=str, default="base",
                        help="Model to use (base, small, medium, etc)")
    args = parser.parse_args()

    run_model_cli(model_name=args.model)
