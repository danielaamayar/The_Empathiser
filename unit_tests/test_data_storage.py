import unittest
import os
import json
import tempfile
import wave
import pandas as pd
import streamlit as st

from data_storage_class import DataStorage

class TestDataStorage(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        st.session_state.clear()
        self.ds = DataStorage(data_collector=self.tempdir.name)
        self.wav_file = os.path.join(self.tempdir.name, "dummy.wav")
        with wave.open(self.wav_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b'\x00' * 16000)  

    def tearDown(self):
        self.tempdir.cleanup()

    def test_save_and_store_demographics(self):
        info = dict(user_name="Alice", age=30, gender="Female", education="Undergrad")
        self.ds.store_user_demographics(info)

        user_folder = os.path.join(self.tempdir.name, "Alice")
        self.assertTrue(os.path.isdir(user_folder))

        csv = os.path.join(user_folder, "Demographic_data.csv")
        df = pd.read_csv(csv)
        self.assertEqual(df.loc[0, "Name"], "Alice")
        self.assertIn("Timestamp", df.columns)
        self.assertEqual(st.session_state.user_folder, user_folder)

    def test_save_emotion_data(self):
        csv = os.path.join(self.tempdir.name, "data.csv")
        probs = {"happy": 50.0, "sad": 50.0}
        self.ds.save_emotion_data(probs, frame_count=1, csv_path=csv)
        df = pd.read_csv(csv)
        self.assertEqual(list(df.columns), ["frame", "happy", "sad"])
        self.assertEqual(df.loc[0, "frame"], 1)
        self.ds.save_emotion_data({"happy": 60.0, "sad": 40.0}, frame_count=2, csv_path=csv)
        df2 = pd.read_csv(csv)
        self.assertEqual(len(df2), 2)

    def test_save_voice_data_success(self):
        st.session_state.clear()
        info = self.ds.save_voice_data(
            user_name="Bob",
            transcription="Hello",
            sentiment="positive",
            scores={"pos": 0.8, "neg": 0.2},
            audio_path=self.wav_file
        )
        self.assertTrue(os.path.exists(info["json_path"]))
        j = json.load(open(info["json_path"]))
        self.assertEqual(j["transcription"], "Hello")
        self.assertTrue(os.path.exists(info["audio_path"]))

    def test_save_voice_data_missing_audio(self):
        with self.assertRaises(FileNotFoundError):
            self.ds.save_voice_data(
                user_name="Bob",
                transcription="Test",
                sentiment="neutral",
                scores={},
                audio_path="nonexistent.wav"
            )

    def test_save_audio_recording_and_metadata(self):
        st.session_state.user_folder = self.tempdir.name
        data = b'\x00' * 32000  
        saved = self.ds.save_audio_recording(audio_bytes=data, recording_type="test")
        self.assertTrue(saved and os.path.exists(saved))

        meta = os.path.join(os.path.dirname(saved), "recordings_metadata.json")
        self.assertTrue(os.path.exists(meta))
        arr = json.load(open(meta))
        self.assertEqual(arr[0]["type"], "test")
        self.assertEqual(arr[0]["filename"].startswith("test_"), True)

    def test_save_audio_without_demographics(self):
        if hasattr(st.session_state, "user_folder"):
            del st.session_state.user_folder
        res = self.ds.save_audio_recording(audio_bytes=b"", recording_type="test")
        self.assertIsNone(res)

if __name__ == "__main__":
    unittest.main()
