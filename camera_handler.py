import cv2
import time
import streamlit as st

class CameraHandler:
    def __init__(self):
        self.capture = None
        self.running = False

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            st.error("Error: Could not open webcam.")
            return False
        self.running = True
        return True

    def stop_camera(self):
        if self.capture:
            self.capture.release()
        cv2.destroyAllWindows()
        self.running = False

    def capture_frames(self, detection_key, process_frame_callback):
        frame_count = 0
        while self.running and self.capture.isOpened():
            ret, frame = self.capture.read()
            if not ret or not self.running:
                break

            process_frame_callback(frame, frame_count, detection_key)
            frame_count += 1
            time.sleep(1)

        self.stop_camera()
