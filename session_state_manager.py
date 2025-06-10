import streamlit as st

class SessionStateManager:
    
    def __init__(self):
        self.defaults = {
            "camera_active": False,
            "running": False,
            "video_capture": None,
            
            "user_folder": None,
            "folder": None,
            "csv_path": None,
            "start_pressed": False,
            
            "video1_intensity": 0,
            "video1_sadness": 0,
            "video1_upset": 0,
            "video1_bad_action": 0,
            "video1_punishment": 0,
            
            "video2_intensity": 0,
            "video2_happy": 0,
            "video2_pleased": 0,
            "video2_good_action": 0,
            "video2_encourage": 0,
            
            "news1_intensity": 0,
            "news1_happy": 0,
            "news1_pleased": 0,
            "news1_good_action": 0,
            "news1_encourage": 0,
            
            "news2_intensity": 0,
            "news2_sadness": 0,
            "news2_upset": 0,
            "news2_bad_action": 0,
            "news2_punishment": 0,
            
            "start_pressed_video1": False,
            "start_pressed_video2": False,
            "start_pressed_news1": False,
            "start_pressed_news2": False
        }
        self.state = st.session_state
    

    def init(self, key, default):
        if key not in self.state:
            self.state[key] = default

    def get(self, key):
        return self.state.get(key)

    def set(self, key, value):
        self.state[key] = value

    def init_all(self):
        for key, value in self.defaults.items():
            self.init(key, value)
    
print(dir(SessionStateManager))