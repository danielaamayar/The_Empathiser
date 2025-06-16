import streamlit as st
import torch 
from data_storage_class import DataStorage
from emotion_detector import EmotionDetector
from camera_handler import CameraHandler
from emotion_manager import EmotionSessionManager
from voice_sentiment import VoiceAnalysis
from paths import ProjectPaths
from emotion_colours import emotion_colours as colours
from questionnaire import QuestionnaireManager
from session_state_manager import SessionStateManager
from user_interaction import UI

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
paths = ProjectPaths()
session = SessionStateManager()
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
session = SessionStateManager()
session.init_all()
user_interaction = UI(session=session, session_manager=session_manager, questionnaire_manager=questionnaire_manager)
voice_analyzer = VoiceAnalysis(device=device)


content_paths = {
    "Video 1": str(paths.video1_path),
    "Video 2": str(paths.video2_path),
    "Article 1": str(paths.article1_path),
    "Article 2": str(paths.article2_path) 
}

st.markdown("""<style>.stApp {background-color: #F6F6EE;  /* Replace with your desired color */}</style>""",
    unsafe_allow_html=True)

st.title("The Empathiser")
st.caption("Welcome to the Empathiser. You are about to participate in an academic research study focused on emotional responses to environmental content. " \
"Your participation is entirely voluntary, and you may withdraw at any time without any consequences. All data collected, including facial expression and voice recordings, will be handled confidentially and in accordance with ethical research standards. "

"We appreciate your contribution to this study.")
st.caption("Before we begin, we will ask you to provide some personal information.")
st.header("Personal data")
user_name = st.text_input("Enter your full name", key="user_name")

if user_name:
    age = st.number_input("Enter your age", min_value=0, max_value=120, step=1, key="age")
    gender = st.selectbox("Select your gender", ["Male", "Female", "Non-binary / Third gender", "Other", "Prefer not to say"], key="gender")
    education = st.selectbox("Select your highest educational level", [
        "No formal education", "Primary education", "Secondary education",
        "Technical or vocational training", "Undergraduate degree", "Graduate degree (Master's, Ph.D., etc.)"
    ], key="education")

    st.caption("Press the button to continue.")

    if st.button("Submit"):
        user_info = {
            "user_name": user_name,
            "age": age,
            "gender": gender,
            "education": education
        }
        data_storage.store_user_demographics(user_info)
        st.success("Thank you!")

    st.header("Let's get to it")
    st.caption("You will be shown two short videos and two news articles. Please watch or read them and react as naturally as possible.")

    st.write("------------------------------------------------------------------------------")

    # Video 1 Section
    st.subheader("Step 1: Watch The First Video")
    st.caption("Please press 'Done' once you have watched the video.")

    user_interaction.show_video_step("Video 1", content_paths["Video 1"])


    st.write("------------------------------------------------------------------------------")

    st.subheader("Step 2: Read This News Article")
    st.caption("You will be shown a short segment presenting information that has appeared in the news. Please engage with the content and react as naturally as possible.")
    st.caption("Please press 'Done' once you have read the article.")
    user_interaction.show_article_step("News 1", content_paths["Article 1"], is_positive=True)

    st.write("------------------------------------------------------------------------------")

    # Video 2 section
    st.subheader("Step 3: Watch The Second Video")
    st.caption("Please press 'Done' once you have watched the video.")
    user_interaction.show_video_step_2("Video 2", content_paths["Video 2"])


    # News article 2 
    st.subheader("Step 4: Read This News Article")
    st.caption("You will be shown a short segment presenting information that has appeared in the news. Please engage with the content and react as naturally as possible.")
    user_interaction.show_news_step_2("News 2", content_paths["Article 2"], is_positive=True)

    st.write("------------------------------------------------------------------------------")
    
    # Voice recording 
    st.subheader("Step 5: Voice thoughts")
    st.caption("Describe your thoughts about what you’ve seen and the messages that resonated with you most deeply.")
    user_interaction.show_voice_input_step(data_storage, voice_analyzer)

    st.caption("Thank you for your participation!")

st.write("------------------------------------------------------------------------------")
    
st.caption("If you have any questions you can contact us at: igomati@javeriana.edu.co, mariaandreamoreno@gmail.com or danielaamayar@gmail.com")