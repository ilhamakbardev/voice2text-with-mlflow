import streamlit as st
from pathlib import Path
import os

from utils.transcriber import transcribe_audio
from utils.recorder_streamlit import record_audio_dynamic_streamlit

st.set_page_config(page_title="🎤 Voice2Text Chat", layout="centered")
st.title("🎙️ Voice to Text Chatbox")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["text"])

DEPLOYED = os.environ.get("STREAMLIT_CLOUD", False)

if not DEPLOYED:
    if st.button("🎤 Start Talking"):
        try:
            

            workspace_audio_dir = Path("audio_recorded")
            workspace_audio_dir.mkdir(parents=True, exist_ok=True)
            audio_path = workspace_audio_dir / "recording_streamlit.wav"

            record_audio_dynamic_streamlit(str(audio_path))

            st.success("✅ Done recording. Transcribing now...")

            with st.spinner("📝 Transcribing..."):
                text = transcribe_audio(str(audio_path), model_name="base")

            st.session_state.messages.append({"role": "user", "text": text})
            st.chat_message("user").markdown(text)

        except ImportError:
            st.error("❌ Error: PyAudio not installed or not working. Live microphone input is not available.")
        except Exception as e:
            st.error(f"❌ Error during recording or transcription: {e}")
else:
    st.info("Live microphone input is not directly supported in this deployed environment. Please upload an audio file instead.")
    audio_file = st.file_uploader("🎤 Upload an audio file", type=["wav", "mp3", "ogg", "flac"])
    if audio_file:
        try:
            st.success("✅ Audio file uploaded. Transcribing now...")
            with st.spinner("📝 Transcribing..."):
                temp_audio_path = Path("uploaded_audio")
                temp_audio_path.mkdir(parents=True, exist_ok=True)
                uploaded_file_path = temp_audio_path / audio_file.name
                with open(uploaded_file_path, "wb") as f:
                    f.write(audio_file.read())

                text = transcribe_audio(str(uploaded_file_path), model_name="base")

            st.session_state.messages.append({"role": "user", "text": text})
            st.chat_message("user").markdown(text)

            import os
            os.remove(uploaded_file_path)

        except Exception as e:
            st.error(f"❌ Error during transcription: {e}")