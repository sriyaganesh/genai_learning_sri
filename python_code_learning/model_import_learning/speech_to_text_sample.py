import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa

# Model name
model_id = "openai/whisper-small"

# Load processor and model
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)

# Load audio file (wav/mp3)
audio_path = "speech_to_text_file.mp3"

speech, sr = librosa.load(audio_path, sr=16000)

# Preprocess
inputs = processor(speech, sampling_rate=16000, return_tensors="pt")

# Generate transcription
with torch.no_grad():
    generated_ids = model.generate(inputs["input_features"])

# Decode
transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)

print("Transcription:")
print(transcription[0])