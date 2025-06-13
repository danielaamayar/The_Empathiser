import os
import pandas as pd
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
import os
import wave
from datetime import datetime
from typing import Dict, Any, Optional
from emotion_colours import emotion_colours



class DataStorage:
    def __init__(self, data_collector):
        self.data_collector = data_collector

    def save_demographic_data(self, user_name, age, gender, education):
        user_folder = os.path.join(self.data_collector, user_name)
        os.makedirs(user_folder, exist_ok=True)
        
        data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": user_name,
            "Age": age,
            "Gender": gender,
            "Education": education
        }
         
        filepath = os.path.join(user_folder, "Demographic_data.csv")
        
        df = pd.DataFrame([data])
        df.to_csv(filepath, index=False)
        st.session_state.user_folder = user_folder  

    def store_user_demographics(self, user_info: Dict[str, Any]) -> None:
        """Store demographics and initialize user folder session."""
        self.save_demographic_data(
            user_name=user_info["user_name"],
            age=user_info["age"],
            gender=user_info["gender"],
            education=user_info["education"]
        )
    
    def save_slider_responses(self, content_type: str, content_name: str, responses: dict):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        folder_name = content_name.replace(" ", "_")
        folder = os.path.join(st.session_state.user_folder, folder_name)
        os.makedirs(folder, exist_ok=True)
        
        data = {"Timestamp": timestamp}
        data.update(responses)  
        
        filename = f"Answers_{folder_name}.csv"
        filepath = os.path.join(folder, filename)
        
        if not os.path.exists(filepath):
            df = pd.DataFrame(columns=data.keys())
        else:
            df = pd.read_csv(filepath)
        
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(filepath, index=False)

    
    def save_emotion_plot(self, face_image, probabilities, frame_count, folder, colours):
     
        palette = [colours[label] for label in probabilities.keys()]
        
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].imshow(np.array(face_image))
        axs[0].axis('off')

        sns.barplot(ax=axs[1],
                    y=list(probabilities.keys()),
                    x=[prob for prob in probabilities.values()],
                    palette=palette,
                    orient='h')
        axs[1].set_xlabel('Probability (%)')
        axs[1].set_title('Emotion Probabilities')
        axs[1].set_xlim([0, 100])

        plot_path = os.path.join(folder, f'frame_{frame_count}.png')
        fig.savefig(plot_path)
        plt.close(fig)


    def save_emotion_data(self, probabilities, frame_count, csv_path):
        data = {**{"frame": frame_count}, **probabilities}
        df = pd.DataFrame([data])
        
        if os.path.exists(csv_path):
            df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)

    def save_voice_data(
        self,
        user_name: str,
        transcription: str,
        sentiment: str,
        scores: Dict[str, float],
        audio_path: str
    ) -> Dict[str, str]:

        try:
            if not all([user_name, isinstance(transcription, str), audio_path]):
                raise ValueError("Missing required parameters")

            user_folder = os.path.join(self.data_collector, user_name)
            voice_folder = os.path.join(user_folder, "voice_data")  
            os.makedirs(voice_folder, exist_ok=True)

            data = {
                "timestamp": datetime.now().isoformat(),
                "transcription": transcription,
                "sentiment": sentiment,
                "scores": scores,
                "audio_file": "recording.wav"  
            }

            json_path = os.path.join(voice_folder, "voice_analysis.json") 
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            saved_audio_path = os.path.join(voice_folder, "recording.wav")
            if os.path.exists(audio_path):
                with open(audio_path, "rb") as src, open(saved_audio_path, "wb") as dst:
                    dst.write(src.read())
            else:
                raise FileNotFoundError(f"Source audio file not found: {audio_path}")

            return {
                "json_path": json_path,
                "audio_path": saved_audio_path,
                "voice_folder": voice_folder
            }

        except Exception as e:
            st.error(f"Failed to save voice data: {str(e)}")
            raise

    def save_audio_recording(self, audio_bytes: bytes, recording_type: str) -> Optional[str]:
        try:
            if not hasattr(st.session_state, 'user_folder'):
                raise ValueError("User session not initialized - complete demographic info first")

            recordings_dir = os.path.join(st.session_state.user_folder, "audio_recordings")
            os.makedirs(recordings_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{recording_type}_{timestamp}.wav"
            filepath = os.path.join(recordings_dir, filename)

            with open(filepath, "wb") as f:
                f.write(audio_bytes)

            actual_duration = self._verify_audio_duration(filepath)
            st.write(f"Saved audio duration: {actual_duration:.2f} seconds")

            self._save_recording_metadata(filepath, recording_type)

            return filepath

        except Exception as e:
            st.error(f"Audio save failed: {str(e)}")
            return None

    def _verify_audio_duration(self, filepath: str) -> float:
        with wave.open(filepath, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)

    def _save_recording_metadata(self, filepath: str, recording_type: str) -> None:
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "type": recording_type,
            "filename": os.path.basename(filepath),
            "path": filepath,
            "size_bytes": os.path.getsize(filepath),
            "format": "WAV",
            "channels": 1,
            "sample_width": 2,
            "sample_rate": 16000
        }

        metadata_path = os.path.join(os.path.dirname(filepath), "recordings_metadata.json")
        
        try:
            existing = []
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    existing = json.load(f)

            existing.append(metadata)

            with open(metadata_path, 'w') as f:
                json.dump(existing, f, indent=2)

        except Exception as e:
            st.warning(f"Could not update recording metadata: {str(e)}")