import os
import datetime
import streamlit as st

class EmotionSessionManager:
    def __init__(self, camera_handler, data_storage, detector, colours):
        self.camera_handler = camera_handler
        self.data_storage = data_storage
        self.detector = detector
        self.colours = colours

    def start_session(self, detection_key):
        if not self.camera_handler.start_camera():
            st.session_state.camera_active = False
            return

        st.session_state.running = True
        st.session_state.camera_active = True

        folder = os.path.join(st.session_state.user_folder, detection_key.replace(" ", "_"))
        os.makedirs(folder, exist_ok=True)
        st.session_state.folder = folder

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        st.session_state.csv_path = os.path.join(folder, f"{timestamp}_emotion_data.csv")

        self.camera_handler.capture_frames(
            detection_key=detection_key,
            process_frame_callback=lambda frame, count, key: self.process_frame(frame, count, key)
        )

    def stop_session(self):
        st.session_state.running = False
        st.session_state.camera_active = False
        self.camera_handler.stop_camera()

    def process_frame(self, frame, frame_count, detection_key):
        print(f"Processing frame {frame_count}...")  

        face, class_probabilities = self.detector.detect_emotion(frame)

        if face is not None and class_probabilities is not None:
            folder = os.path.join(st.session_state.user_folder, detection_key.replace(" ", "_"))

            csv_path = st.session_state.csv_path

            self.data_storage.save_emotion_plot(
                face_image=face,
                probabilities=class_probabilities,
                frame_count=frame_count,
                folder=folder,
                colours=self.colours
            )

            self.data_storage.save_emotion_data(
                probabilities=class_probabilities,
                frame_count=frame_count,
                csv_path=csv_path,
            )
        else:
            print(f"No face detected in frame {frame_count}")


