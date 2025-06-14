import streamlit as st
import torch
import speech_recognition as sr
from paths import ProjectPaths
from session_state_manager import SessionStateManager
from data_storage_class import DataStorage
from emotion_detector import EmotionDetector
from camera_handler import CameraHandler
from emotion_manager import EmotionSessionManager
from questionnaire import QuestionnaireManager
import os
import pandas as pd
from datetime import datetime
from voice_sentiment import VoiceAnalysis 

colours = {
    "angry": "red",
    "disgust": "green",
    "fear": "gray",
    "happy": "yellow",
    "neutral": "purple",
    "sad": "blue",
    "surprise": "orange"
}
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
paths = ProjectPaths()
session = SessionStateManager()
session.init_all()
data_storage = DataStorage(
    data_collector=str(paths.data_dir)
)
detector = EmotionDetector(device=device)
camera_handler = CameraHandler()
session_manager = EmotionSessionManager(
    camera_handler=camera_handler,
    data_storage=data_storage,
    detector=detector,
    colours=colours
)
questionnaire_manager = QuestionnaireManager(data_storage=data_storage)
voice_analyzer = VoiceAnalysis(device=device)

content_paths = {
    "Video 1": str(paths.video1_path),
    "Video 2": str(paths.video2_path),
    "Article 1": str(paths.article1_path),
    "Article 2": str(paths.article2_path) 
}


#Settings for background colour 
#st.markdown("""<style>.stApp {background-color: #F6F6EE;  /* Replace with your desired color */}</style>""",
    #unsafe_allow_html=True)

st.title("Empathiser")
st.caption("TEXT.")
st.caption("Before we begin, we will ask you to provide some personal information.")
st.header("Personal data")
user_name = st.text_input("Enter your full name", key="user_name")

if user_name:
    pass

    age = st.number_input("Enter your age", min_value=0, max_value=120, step=1, key="age")
    gender = st.selectbox("Select your gender", ["Male", "Female", "Non-binary / Third gender", "Other", "Prefer not to say"], key="gender")
    education = st.selectbox("Select your highest educational level", [
        "No formal education", "Primary education", "Secondary education",
        "Technical or vocational training", "Undergraduate degree", "Graduate degree (Master's, Ph.D., etc.)"
    ], key="education")

    st.caption("Press the button to continue.")

    if st.button("Submit"):
        data_storage.save_demographic_data(
            user_name=user_name,
            age=age,
            gender=gender,
            education=education
        )
        st.session_state.user_folder = os.path.join(data_storage.data_collector, user_name)

        st.success("Thank you!")
    
    st.header("Let's get to it")
    st.caption("TEXT.")

    st.write("------------------------------------------------------------------------------")

    # Video 1 Section
    st.subheader("Step 1: Watch The First Video")
    st.caption("Please press 'Done' once you have watched the video.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show me the video", key="start_video1"):
            st.session_state.showing_video1 = True
            st.session_state.answering_video1 = False
            st.rerun()

    with col2:
        if st.session_state.get('showing_video1') and st.button("Done", key="stop_video1"):
            st.session_state.answering_video1 = True
            st.session_state.showing_video1 = False
            st.rerun()

    if st.session_state.get('showing_video1'):
        st.video(content_paths["Video 1"])
        session_manager.start_session("Video 1")

    st.caption("Please press 'Done' once you have watched the video.")

    if st.session_state.get('answering_video1'):
        questionnaire_manager.show_video_questions("Video 1")


    st.write("------------------------------------------------------------------------------")

    # News article 1 section
    st.subheader("Step 2: Read This News Article")
    st.caption("Please press 'Done' once you have read the article.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show me the article", key="news_article1"):
            st.session_state.showing_news1 = True
            st.session_state.answering_news1 = False
            st.rerun()

    with col2:
        if st.session_state.get('showing_news1') and st.button("Done", key="done_news1"):
            st.session_state.answering_news1 = True
            st.session_state.showing_news1 = False
            st.rerun()

    if st.session_state.get('showing_news1'):
        article_path = content_paths["Article 1"]
        try: 
            with open(article_path, "r", encoding="utf-8") as file:
                article_text = file.read()
                st.markdown(article_text)
        except FileNotFoundError:
            st.error("Article file not found. Please check the path.")        
        session_manager.start_session("News 1")

    st.caption("Please press 'Done' once you have read the article.")

    if st.session_state.get('answering_news1'):
        questionnaire_manager.show_news_questions("News 1", is_positive=True)


    st.write("------------------------------------------------------------------------------")

    # Video 2 section
    st.subheader("Step 3: Watch The Second Video")
    st.caption("Please press 'Done' once you have watched the video.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show me the video", key="start_video2"):
            st.session_state.showing_video2 = True  # <- FIXED
            st.session_state.answering_video2 = False
            st.rerun()
    
    with col2:
        if st.session_state.get('showing_video2') and st.button("Done", key="stop_video2"):
            st.session_state.answering_video2 = True
            st.session_state.showing_video2 = False
            st.rerun()
        
    if st.session_state.get('showing_video2'):
        st.video(content_paths["Video 2"])
        session_manager.start_session("Video 2")
    
    st.caption("Please press 'Done' once you have watched the video.")

    if st.session_state.get('answering_video2'):
        questionnaire_manager.show_video_questions("Video 2")


    # News article 2 
    st.subheader("Step 4: Read This News Article")
    st.caption("TEXT.")
    st.caption("Please press 'Done' once you have read the article.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show me the article", key="news_article2"):
            st.session_state.showing_news2 = True
            st.session_state.answering_news2 = False
            st.rerun()
    with col2:
        if st.session_state.get('showing_news2') and st.button("Done", key="done_news2"):
            st.session_state.answering_news2 = True
            st.session_state.showing_news2 = False
            st.rerun()
    if  st.session_state.get('showing_news2'):       
        article2_path = content_paths["Article 2"]
        try:
            with open(article2_path, "r", encoding="utf-8") as file:
                article_text = file.read()
                st.markdown(article_text)
        except FileNotFoundError:
            st.error("Article file not found. Please check the path.")
            
        session_manager.start_session("News 2")
    
    st.caption("Please press 'Done' once you have read the article.")


    if st.session_state.get('answering_news2'):
        questionnaire_manager.show_news_questions("News 2", is_positive=True)

    st.write("------------------------------------------------------------------------------")
    
    st.subheader("Step 5: Voice thoughts")
    st.caption("Describe your thoughts about what you’ve seen and the message that resonated with you most deeply.")

    if 'recording_saved' not in st.session_state:
        st.session_state.recording_saved = False
        st.session_state.saved_audio_path = None

    audio_data = st.audio_input("Press to record your voice.")

    if audio_data and not st.session_state.recording_saved:
        st.audio(audio_data)
        
        if st.button("Save Recording"):
            try:
                audio_bytes = audio_data.read()
                saved_path = data_storage.save_audio_recording(
                    audio_bytes=audio_bytes,  
                    recording_type="voice_feedback"
                )
                st.success(f"Recording saved.")
                st.session_state.recording_saved = True
                st.session_state.saved_audio_path = saved_path
                st.rerun()
                
            except Exception as e:
                st.error(f"Error saving recording: {str(e)}.")

    if st.session_state.recording_saved and st.session_state.saved_audio_path:
        if st.button("Analyse Recording"):
            try:
               with st.spinner("Analysing your voice feedback..."):
                results = voice_analyzer.analyze_recording(
                    audio_path=st.session_state.saved_audio_path,
                    user_folder=st.session_state.user_folder
                    )
                st.success("Analysis complete! Thank you so much!")
            except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

st.write("------------------------------------------------------------------------------")
    
st.caption("Thank you for your participation. If you have any questions you can contact us at: igomati@javeriana.edu.co, mariaandreamoreno@gmail.com or danielaamayar@gmail.com")