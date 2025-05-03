import streamlit as st
from utils.transcriber import transcribe_audio
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import platform
import queue

ffmpeg_dirs = {
    "Windows": "ffmpeg/windows",
    "Linux": "ffmpeg/linux",
    "Darwin": "ffmpeg/macos"
}
ffmpeg_dir = ffmpeg_dirs.get(platform.system())
if ffmpeg_dir:
    os.environ["PATH"] = os.path.abspath(
        ffmpeg_dir) + os.pathsep + os.environ.get("PATH", "")

st.set_page_config(page_title="🎤 Voice2Text Chat", layout="centered")
st.title("🎙️ Voice to Text Chatbox")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["text"])


def record_with_silence_detection(samplerate=16000, silence_thresh=0.01, silence_duration=2.5):
    q_audio = queue.Queue()
    silence_start = None
    recorded_chunks = []

    def callback(indata, frames, time, status):
        nonlocal silence_start
        volume = np.linalg.norm(indata)
        q_audio.put(indata.copy())

        if volume > silence_thresh:
            silence_start = None
        else:
            if silence_start is None:
                silence_start = time.inputBufferAdcTime
            elif time.inputBufferAdcTime - silence_start > silence_duration:
                raise sd.CallbackStop()

    with sd.InputStream(callback=callback, channels=1, samplerate=samplerate):
        try:
            while True:
                chunk = q_audio.get()
                recorded_chunks.append(chunk)
        except sd.CallbackStop:
            pass

    return np.concatenate(recorded_chunks, axis=0)


if st.button("🎤 Start Recording"):
    st.info("🔴 Recording... Speak now!")

    try:
        audio = record_with_silence_detection()

        if audio.size == 0:
            st.error("❌ Tidak ada suara terdeteksi.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                sf.write(f.name, audio, samplerate=16000, subtype='PCM_16')
                audio_path = f.name

            with st.spinner("📝 Transcribing..."):
                text = transcribe_audio(audio_path, model_name="base")
                os.remove(audio_path)

                if not text.strip():
                    st.warning("⚠️ Tidak ada teks yang ditranskripsi.")
                else:
                    st.session_state.messages.append(
                        {"role": "user", "text": text})
                    st.chat_message("user").markdown(text)

    except Exception as e:
        st.error(f"❌ Error: {e}")
