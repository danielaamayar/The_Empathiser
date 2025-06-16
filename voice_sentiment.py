import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import speech_recognition as sr
from typing import Tuple, Dict, Any
import json
from datetime import datetime


class VoiceAnalysis:
    def __init__(self, device: str = None):

        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        self.recognizer = sr.Recognizer()
        
        model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
        self.labels = ['Negative', 'Neutral', 'Positive']
    
#ChatGPT assisted in writing these exceptions. 
    def transcribe_audio(self, audio_path: str) -> str:
        try:
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                return text
        except sr.UnknownValueError:
            raise Exception("The Empathiser could not understand the audio.")
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def predict_sentiment(self, text: str) -> Tuple[str, Dict[str, float]]:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        
        with torch.no_grad():
            logits = self.model(**inputs).logits
        
        probs = torch.nn.functional.softmax(logits, dim=1)[0]
        sentiment = self.labels[probs.argmax()]
        
        scores = {label: float(prob) for label, prob in zip(self.labels, probs.cpu().numpy())}
        
        return sentiment, scores
    
    def analyze_recording(self, audio_path: str, user_folder: str = None) -> Dict[str, Any]:

        transcription = self.transcribe_audio(audio_path)
        
        sentiment, scores = self.predict_sentiment(transcription)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "audio_file": os.path.basename(audio_path),
            "transcription": transcription,
            "sentiment": sentiment,
            "scores": scores,
            "analysis_version": "1.0"
        }
        
        if user_folder:
            self.save_analysis(results, user_folder)
        
        return results
    
    def save_analysis(self, results: Dict[str, Any], user_folder: str) -> str:

        os.makedirs(user_folder, exist_ok=True)
        
        voice_folder = os.path.join(user_folder, "voice_analysis")
        os.makedirs(voice_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_path = os.path.join(voice_folder, f"analysis_{timestamp}.json")
        
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        
        return result_path