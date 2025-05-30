import whisper
import time
import mlflow
from utils.ffmpeg_path import get_ffmpeg_path
import os
import streamlit as st

import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)


def transcribe_audio(audio_path: str, model_name: str):
    ffmpeg_path = get_ffmpeg_path()
    os.environ["PATH"] = os.path.dirname(
        ffmpeg_path) + os.pathsep + os.environ["PATH"]

    model = whisper.load_model(model_name)

    st.info(f"Using device: {device.upper()}")

    start = time.time()
    result = model.transcribe(audio_path, language="indonesian")
    duration = time.time() - start

    text = result["text"]

    mlflow.log_param("model_name", model_name)
    mlflow.log_metric("inference_time", duration)
    mlflow.log_text(text, "transcription.txt")

    return text
