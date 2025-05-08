import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import time
from pathlib import Path
import streamlit as st


def record_audio_dynamic_streamlit(filepath: str, silence_threshold=0.015, silence_duration=2, sample_rate=16000):
    st.info("🎙️ Waiting for sound to start recording...")

    q_audio = queue.Queue()
    recording = []
    is_recording = False
    silence_start = None

    def callback(indata, frames, time_info, status):
        q_audio.put(indata.copy())

    with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
        while True:
            audio_chunk = q_audio.get()
            volume_norm = np.linalg.norm(audio_chunk)

            if volume_norm > silence_threshold:
                if not is_recording:
                    st.info("🔴 Sound detected, recording started...")
                    is_recording = True
                recording.append(audio_chunk)
                silence_start = None

            elif is_recording:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start >= silence_duration:
                    st.info("⏹️ Silence detected, stopping recording.")
                    break

    audio_np = np.concatenate(recording, axis=0)
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(filepath), audio_np, sample_rate)
    st.info(f"✅ Saved to {filepath}")
