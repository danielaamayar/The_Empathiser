import streamlit as st
from data_storage_class import DataStorage

class QuestionnaireManager:
    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage
        
    def show_video_questions(self, video_name: str):
        st.subheader(f"Answer Some Questions about {video_name}")
        st.caption("Please answer the following questions based on the video you just watched. Respond as honestly and accurately as possible according to your personal experience.")
        if f"{video_name}_responses" not in st.session_state:
            st.session_state[f"{video_name}_responses"] = {
                "sadness": 50,
                "upset": 50,
                "bad_action": 50,
                "punishment": 50
            }
        
        st.session_state[f"{video_name}_responses"]["sadness"] = st.slider(
            "How sad do you feel about what is happening in the video? (0 = Not sad, 100 = Very sad)", 
            0, 100, 
            value=st.session_state[f"{video_name}_responses"]["sadness"],
            key=f"{video_name}_sadness"
        )
        
        st.session_state[f"{video_name}_responses"]["upset"] = st.slider(
            "How upset do you feel about what is happening in the video? (0 = Not upset, 100 = Very upset)", 
            0, 100,
            value=st.session_state[f"{video_name}_responses"]["upset"],
            key=f"{video_name}_upset"
        )
        
        st.session_state[f"{video_name}_responses"]["bad_action"] = st.slider(
            "How bad was the action performed in the video? (0 = Not bad, 100 = Very bad)", 
            0, 100,
            value=st.session_state[f"{video_name}_responses"]["bad_action"],
            key=f"{video_name}_bad_action"
        )
        
        st.session_state[f"{video_name}_responses"]["punishment"] = st.slider(
            "How much punishment does the action shown in the video deserve? (0 = No punishment, 100 = Severe punishment)", 
            0, 100,
            value=st.session_state[f"{video_name}_responses"]["punishment"],
            key=f"{video_name}_punishment"
        )

        if st.button(f"Submit answers for {video_name}"):
            self.data_storage.save_slider_responses("video", video_name, st.session_state[f"{video_name}_responses"])
            st.success("Responses saved!")
            return True
        return False

    def show_news_questions(self, news_name: str, is_positive: bool = True):
        st.subheader(f"Answer Some Questions about {news_name}")
        st.caption("Please answer the following questions based on the news article you just read.")
        if f"{news_name}_responses" not in st.session_state:
            if is_positive:
                st.session_state[f"{news_name}_responses"] = {
                    "happy": 50,
                    "pleased": 50,
                    "good_action": 50,
                    "encourage": 50
                }
            else:
                st.session_state[f"{news_name}_responses"] = {
                    "sad": 50,
                    "upset": 50,
                    "bad": 50,
                    "punishment": 50
                }
        
        if is_positive:
            st.session_state[f"{news_name}_responses"]["happy"] = st.slider(
                "How happy do you feel about what is described in the news article?",
                0, 100,
                value=st.session_state[f"{news_name}_responses"]["happy"],
                key=f"{news_name}_happy"
            )
            
            st.session_state[f"{news_name}_responses"]["pleased"] = st.slider(
                "How pleased do you feel about what is described in the news article?",
                0, 100,
                value=st.session_state[f"{news_name}_responses"]["pleased"],
                key=f"{news_name}_pleased"
            )
            
            st.session_state[f"{news_name}_responses"]["good_action"] = st.slider(
                "How good do you think the actions described in the news article were?",
                0, 100,
                value=st.session_state[f"{news_name}_responses"]["good_action"],
                key=f"{news_name}_good_action"
            )
            
            st.session_state[f"{news_name}_responses"]["encourage"] = st.slider(
                "To what extent would you encourage these kinds of actions?",
                0, 100,
                value=st.session_state[f"{news_name}_responses"]["encourage"],
                key=f"{news_name}_encourage"
            )
        else:
            st.session_state[f"{news_name}_responses"]["sad"] = st.slider(
                "How sad do you feel about what is described in the news article? (0 = Not sad, 100 = Very sad)", 
                0, 100,
                value=st.session_state[f"{news_name}_responses"]["sad"],
                key=f"{news_name}_sad"
            )
            
            st.session_state[f"{news_name}_responses"]["upset"] = st.slider(
                "How upset do you feel about what is described in the news article? (0 = Not upset, 100 = Very upset)", 
                0, 100,
                value=st.session_state[f"{news_name}_responses"]["upset"],
                key=f"{news_name}_upset"
            )
            
            st.session_state[f"{news_name}_responses"]["bad"] = st.slider(
                "How bad do you think the situation reported in the news article was? (0 = Not bad, 100 = Very bad)", 
                0, 100,
                value=st.session_state[f"{news_name}_responses"]["bad"],
                key=f"{news_name}_bad"
            )
            
            st.session_state[f"{news_name}_responses"]["punishment"] = st.slider(
                "How much punishment do you think the situation described in the news article deserves? (0 = No punishment, 100 = Severe punishment)", 
                0, 100,
                value=st.session_state[f"{news_name}_responses"]["punishment"],
                key=f"{news_name}_punishment"
            )

        if st.button(f"Submit answers for {news_name}"):
            self.data_storage.save_slider_responses("news", news_name, st.session_state[f"{news_name}_responses"])
            st.success("Responses saved!")
            return True
        return False