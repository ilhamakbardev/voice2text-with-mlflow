# 🗣️ Voice2Text - MLflow Whisper Evaluation

This project allows you to **record Indonesian speech**, **transcribe it using OpenAI's Whisper models**, and **evaluate transcription performance** with MLflow tracking. it run locally.

---

## 📦 Features

- 🎙️ Record audio samples directly from CLI
- 🧠 Transcribe using Whisper models (`base`, `small`, `medium`)
- 📊 Log metrics and artifacts to MLflow
- 📈 Visualize model performance (inference time, WER)
- 🧪 Compare models via `eval_all_models.py`
- 💻 **Cross-platform** : works on **Windows**, **macOS**, and **Linux**.

---

## 🚀 Quickstart (Recommended: Use Python 3.11.9 with .venv)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Testing single model

```bash
python main.py --model small
```

Available options for params --model :

- base (default)
- small
- medium

The script will:

- Record 5 seconds of audio from mic
- Transcribe the audio using the selected model
- Print the result to terminal
- Log the audio and output to MLflow (Default Experiment)

### 3. Evaluate all models

Record once and evaluate using all models:

```bash
python eval_all_models.py
```

This will:

- Record 5 seconds of audio from mic
- Run transcription with each model
- Log metrics (inference_time, text length)
- Save results to MLflow under the voice2text-eval experiment

### 4. Start MLflow UI

Launch the MLflow dashboard locally:

```bash
mlflow ui
```

Then open http://127.0.0.1:5000 to view experiment results or compare model.
