import sounddevice as sd
from scipy.io.wavfile import write


def record_audio(path: str, duration: int = 5, fs: int = 44100):
    print(f"🎙️ Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs,
                       channels=1, dtype='float32')
    sd.wait()
    write(path, fs, recording)
    print(f"✅ Saved recording to {path}")
