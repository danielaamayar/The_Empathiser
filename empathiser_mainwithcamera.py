import streamlit as st
import torch
import os
import datetime
from session_state_manager import SessionStateManager
from data_storage_class import DataStorage
from emotion_detector import EmotionDetector
from camera_handler import CameraHandler


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
session = SessionStateManager()
session.init_all()
detector = EmotionDetector(device=device)
camera_handler = CameraHandler()
data_storage = DataStorage(
    data_collector="/Users/danielaamayarueda/Documents/GitHub/AI-4-Media-Project-Daniela-Amaya/Data" 
)
colours = {
    "angry": "red",
    "disgust": "green",
    "fear": "gray",
    "happy": "yellow",
    "neutral": "purple",
    "sad": "blue",
    "surprise": "orange"
}

# Environmental videos to reproduce 
video_paths = {
    "Video 1": "Garbage.mov",
    "Video 2": "/Users/danielaamayarueda/Documents/GitHub/AI-4-Media-Project-Daniela-Amaya/Environmental_videos/Playing_cows.mp4"
}

# This function open's the camera input recording and captures the frames 1 * second 
def detect_emotion(detection_key):
    if not camera_handler.start_camera():
        st.session_state.camera_active = False
        return

    st.session_state.running = True
    st.session_state.camera_active = True

    camera_handler.capture_frames(
        detection_key=detection_key,
        process_frame_callback=lambda frame, count, key: frame_emotion_detection(
            frame, count, key, data_storage, colours, detector
        )
    )

# This function handles frames processing 
def start_emotion_detection(detection_key):
    if not st.session_state.camera_active:
        folder = os.path.join(st.session_state.user_folder, detection_key.replace(" ", "_"))
        os.makedirs(folder, exist_ok=True)
        st.session_state.folder = folder

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        st.session_state.csv_path = os.path.join(folder, f"{timestamp}_emotion_data.csv")

        st.session_state.camera_active = True
        detect_emotion(detection_key)

#This function stops the ongoing emotion detection process and releases the webcam
def stop_emotion_detection():
    st.session_state.running = False
    st.session_state.camera_active = False
    camera_handler.stop_camera()

def frame_emotion_detection(frame, frame_count, detection_key, data_storage, colours, detector):
    print(f"Processing frame {frame_count}...")  # Add this line

    face, class_probabilities = detector.detect_emotion(frame)

    if face is not None and class_probabilities is not None:
        folder = os.path.join(st.session_state.user_folder, detection_key.replace(" ", "_"))
        os.makedirs(folder, exist_ok=True)

        csv_path = st.session_state.csv_path

        data_storage.save_emotion_plot(
            face_image=face,
            probabilities=class_probabilities,
            frame_count=frame_count,
            folder=folder,
            colours=colours
        )

        data_storage.save_emotion_data(
            probabilities=class_probabilities,
            frame_count=frame_count,
            csv_path=csv_path,
        )
    
    else:
        print(f"No face detected in frame {frame_count}")

#Settings for background colour 
st.markdown("""<style>.stApp {background-color: #F6F6EE;  /* Replace with your desired color */}</style>""",
    unsafe_allow_html=True)

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
        st.success("Thank you!")
    
    st.header("Let's get to it")
    st.caption("TEXT.")

    st.write("------------------------------------------------------------------------------")

    # Video 1 section
    st.subheader("Step 1: Watch The First Video")
    st.caption("Please press 'Done' once you have watched the video.")

    if st.button("Show me the video", key="start_video1"):
        st.session_state.start_pressed_video1 = True 
        st.video(video_paths["Video 1"])
        start_emotion_detection("Video 1")
    if st.button("Done", key="stop_video1") and st.session_state.camera_active:
        stop_emotion_detection()
    
    # Video 1 questions 
    st.subheader("Answer Some Questions about Video 1")
    st.caption("Please answer the following questions based on the video you just watched. Respond as honestly and accurately as possible according to your personal experience.")
    video1_sadness = st.slider(
        "How sad do you feel about what is happening in the video? (0 = Not sad, 100 = Very sad)", 
        0, 100, 
        key="video1_sadness"
    )
    video1_upset = st.slider(
        "How upset do you feel about what is happening in the video? (0 = Not upset, 100 = Very upset)", 
        0, 100, 
        key="video1_upset"
    )
    video1_bad_action = st.slider(
        "How bad was the action performed in the video? (0 = Not bad, 100 = Very bad)", 
        0, 100, 
        key="video1_bad_action"
    )
    video1_punishment = st.slider(
        "How much punishment does the action shown in the video deserve? (0 = No punishment, 100 = Severe punishment)", 
        0, 100, 
        key="video1_punishment"
    )

    if st.button("Submit answers", key="submit_video1"):
        data_storage.save_slider_responses("video", "Video 1")

    st.write("------------------------------------------------------------------------------")

    # News article 1 section
    st.subheader("Step 2: Read This News Article")
    st.caption("You will be shown a short segment presenting information that has appeared in the news. Please engage with the content and react as naturally as possible.")
    st.caption("Please press 'Done' once you have read the article.")

    if st.button("Show me the article", key="news_article1"):
        st.session_state.start_pressed_news1 = True  
        st.markdown("""TEXT"""
        )
        start_emotion_detection("News 1")  
    if st.button("Done", key="done_news1") and st.session_state.camera_active:
        stop_emotion_detection()


    # News article 1 questions
    st.subheader("Answer Some Questions about News Article 1")
    st.caption("Please answer the following questions based on the news article you just read.")

    news1_happy = st.slider(
        "How happy do you feel about what is described in the news article?",
        0, 100, 
        key="news1_happy"
    )
    news1_pleased = st.slider(
        "How pleased do you feel about what is described in the news article?",
        0, 100, 
        key="news1_pleased"
    )
    news1_good_action = st.slider(
        "How good do you think the actions described in the news article were?",
        0, 100, 
        key="news1_good_action"
    )
    news1_encourage = st.slider(
        "To what extent would you encourage these kinds of actions?",
        0, 100, 
        key="news1_encourage"
    )

    if st.button("Submit answers", key="submit_news1"):
        data_storage.save_slider_responses("news", "News 1")

    st.write("------------------------------------------------------------------------------")

    # Video 2 section
    st.subheader("Step 3: Watch The Second Video")
    st.caption("Please press 'Done' once you have watched the video.")

    if st.button("Show me the video", key="start_video2"):
        st.session_state.start_pressed_video2 = True  
        st.video(video_paths["Video 2"])
        start_emotion_detection("Video 2")

    if st.button("Done", key="stop_video2") and st.session_state.camera_active:
        stop_emotion_detection()

    # Video 2 questions 
    st.subheader("Answer Some Questions About Video 2")
    st.caption("Please answer the following questions based on the video you just watched. Respond as honestly and accurately as possible according to your personal experience.")
    video2_happy = st.slider(
        "How happy do you feel about what is happening in the video? (0 = Not happy, 100 = Very happy)", 
        0, 100, 
        key="video2_happy"
    )
    video2_pleased = st.slider(
        "How pleased do you feel about what is happening in the video? (0 = Not pleased, 100 = Very pleased)", 
        0, 100, 
        key="video2_pleased"
    )
    video2_good_action = st.slider(
        "How good was the action performed in the video? (0 = Not good, 100 = Very good)", 
        0, 100, 
        key="video2_good_action"
    )
    video2_encourage = st.slider(
        "To what extent would you encourage these kinds of actions? (0 = Not at all, 100 = Strongly encourage)", 
        0, 100, 
        key="video2_encourage"
    )

    if st.button("Submit answers", key="submit_video2"):
        data_storage.save_slider_responses("video", "Video 2")

    # News article 2 
    st.subheader("Step 4: Read This News Article")
    st.caption("TEXT.")
    st.caption("Please press 'Done' once you have read the article.")
    if st.button("Show me the article", key="news_article2"):
        st.session_state.start_pressed_news2 = True  
        st.markdown("""TEXT"""
    )
        start_emotion_detection("News 2")
    if st.button("Done", key="done_news2") and st.session_state.camera_active:
        stop_emotion_detection()

    # News article 2 questions 
    st.subheader("Answer Some Questions about the News Article 2")
    st.caption("Please answer the following questions based on the information you just read. Respond as honestly and accurately as possible according to your personal experience.")

    news2_sad = st.slider(
        "How sad do you feel about what is described in the news article? (0 = Not sad, 100 = Very sad)", 
        0, 100, 
        key="news2_sad"
    )
    news2_upset = st.slider(
        "How upset do you feel about what is described in the news article? (0 = Not upset, 100 = Very upset)", 
        0, 100, 
        key="news2_upset"
    )
    news2_bad = st.slider(
        "How bad do you think the situation reported in the news article was? (0 = Not bad, 100 = Very bad)", 
        0, 100, 
        key="news2_bad"
    )
    news2_punishment = st.slider(
        "How much punishment do you think the situation described in the news article deserves? (0 = No punishment, 100 = Severe punishment)", 
        0, 100, 
        key="news2_punishment"
    )

    if st.button("Submit answers", key="submit_news2"):
        data_storage.save_slider_responses("news", "News 2")

    st.write("------------------------------------------------------------------------------")
    st.caption("Thank you for your participation. If you have any questions you can contact us at: igomati@javeriana.edu.co, mariaandreamoreno@gmail.com or danielaamayar@gmail.com")