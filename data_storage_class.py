import os
import pandas as pd
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class DataStorage:
    def __init__(self, data_collector):
        self.data_collector = data_collector

    def save_demographic_data(self, user_name, age, gender, education):
        user_folder = os.path.join(self.data_collector, user_name)
        os.makedirs(user_folder, exist_ok=True)
        
        data = {
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": user_name,
            "Age": age,
            "Gender": gender,
            "Education": education
        }
        
        filepath = os.path.join(user_folder, "Demographic_data.csv")
        
        df = pd.DataFrame([data])
        df.to_csv(filepath, index=False)
        st.session_state.user_folder = user_folder  

    def save_slider_responses(self, content_name: str, responses: dict):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
