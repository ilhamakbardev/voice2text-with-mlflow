import warnings
import os
import mlflow
from pathlib import Path
from utils.recorder import record_audio_dynamic
from models.base_model import run as run_base
from models.small_model import run as run_small
from models.medium_model import run as run_medium

warnings.filterwarnings("ignore")
os.environ["GIT_PYTHON_REFRESH"] = "quiet"


workspace_audio_dir = Path("audio_recorded")
workspace_audio_dir.mkdir(parents=True, exist_ok=True)
audio_path = workspace_audio_dir / "eval_sample.wav"

record_audio_dynamic(str(audio_path))

mlflow.set_experiment("voice2text-eval")

print("🚀 Evaluating on all models...")

print("➡️ Running base model...")
run_base(audio_path)

print("➡️ Running small model...")
run_small(audio_path)

print("➡️ Running medium model...")
run_medium(audio_path)

print("✅ Done evaluating all models!")
