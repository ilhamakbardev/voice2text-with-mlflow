import streamlit as st
from pathlib import Path

from utils.transcriber import transcribe_audio
from utils.recorder_streamlit import record_audio_dynamic_streamlit


st.set_page_config(page_title="🎤 Voice2Text Chat", layout="centered")
st.title("🎙️ Voice to Text Chatbox")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["text"])


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

    except Exception as e:
        st.error(f"❌ Error: {e}")
