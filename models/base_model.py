from utils.recorder import record_audio
from utils.transcriber import transcribe_audio
import mlflow


def run(audio_path):
    with mlflow.start_run(run_name="Whisper-base"):
        mlflow.log_param("model_name", "base")
        text = transcribe_audio(str(audio_path), model_name="base")
        mlflow.log_metric("text_length", len(text))
        mlflow.log_text(text, "transcription.txt")
        print("📝", text)
