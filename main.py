import os
import platform
import tempfile
import subprocess
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import whisper
import warnings
import argparse
warnings.filterwarnings("ignore", category=UserWarning)


parser = argparse.ArgumentParser()
parser.add_argument("--model_name", default="small")
parser.add_argument("--language", default="indonesian")
parser.add_argument("--beam_size", type=int, default=1)
parser.add_argument("--temperature", type=float, default=0.0)
args = parser.parse_args()


model = whisper.load_model("small")


def get_ffmpeg_path():
    base = os.path.join(os.path.dirname(__file__), "ffmpeg")
    system = platform.system().lower()
    if system == "windows":
        return os.path.join(base, "windows", "ffmpeg.exe")
    elif system == "linux":
        return os.path.join(base, "linux", "ffmpeg")
    elif system == "darwin":
        return os.path.join(base, "macos", "ffmpeg")
    else:
        raise RuntimeError(f"Unsupported platform: {system}")


ffmpeg_path = get_ffmpeg_path()

os.environ["PATH"] = os.path.dirname(
    ffmpeg_path) + os.pathsep + os.environ["PATH"]

fs = 44100
duration = 5

print("🎤 Starting mic-based speech-to-text in Bahasa (Ctrl+C to stop)")

try:
    while True:
        print("\n🔴 Recording...")
        recording = sd.rec(int(duration * fs), samplerate=fs,
                           channels=1, dtype='float32')
        sd.wait()
        audio = np.squeeze(recording)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            write(f.name, fs, audio)
            wav_path = f.name

        mp3_path = wav_path.replace(".wav", ".mp3")

        subprocess.run([ffmpeg_path, "-y", "-i", wav_path, mp3_path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print("🧠 Transcribing...")
        result = model.transcribe(mp3_path, language="indonesian")
        print("📝 Result:", result["text"])

except KeyboardInterrupt:
    print("\n✅ Finished.")
