from utils.transcriber import transcribe_audio
import mlflow


def run(audio_path):
    with mlflow.start_run(run_name="Whisper-medium"):
        mlflow.log_param("model_name", "medium")
        text = transcribe_audio(str(audio_path), model_name="medium")
        mlflow.log_metric("text_length", len(text))
        mlflow.log_text(text, "transcription.txt")
        print("📝", text)
