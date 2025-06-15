
import streamlit as st

class UI:
    def __init__(self, session, session_manager, questionnaire_manager):
        self.session = session
        self.session_manager = session_manager
        self.questionnaire_manager = questionnaire_manager

    def show_video_step(self, video_key, video_path):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Show me the video", key=f"start_{video_key}"):
                self.session.set(f"showing_{video_key}", True)
                self.session.set(f"answering_{video_key}", False)
                st.rerun()

        with col2:
            if self.session.get(f"showing_{video_key}") and st.button("Done", key=f"stop_{video_key}"):
                self.session.set(f"answering_{video_key}", True)
                self.session.set(f"showing_{video_key}", False)
                st.rerun()

        if self.session.get(f"showing_{video_key}"):
            st.video(video_path)
            self.session_manager.start_session(video_key)

        st.caption("Please press 'Done' once you have watched the video.")

        if self.session.get(f"answering_{video_key}"):
            self.questionnaire_manager.show_video_questions(video_key)


    def show_article_step(self, article_key, article_path, is_positive=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Show me the article", key=f"show_{article_key}"):
                self.session.set(f"showing_{article_key}", True)
                self.session.set(f"answering_{article_key}", False)
                st.rerun()

        with col2:
            if self.session.get(f"showing_{article_key}") and st.button("Done", key=f"done_{article_key}"):
                self.session.set(f"answering_{article_key}", True)
                self.session.set(f"showing_{article_key}", False)
                st.rerun()

        if self.session.get(f"showing_{article_key}"):
            try:
                with open(article_path, "r", encoding="utf-8") as file:
                    article_text = file.read()
                    st.markdown(article_text)
            except FileNotFoundError:
                st.error("Article file not found.")

            self.session_manager.start_session(article_key)

        st.caption("Please go up and press 'Done' once you have read the article.")

        if self.session.get(f"answering_{article_key}"):
            self.questionnaire_manager.show_news_questions(article_key, is_positive=is_positive)



    def show_video_step_2(self, video_key, video_path):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Show me the video", key=f"start_{video_key}"):
                self.session.set(f"showing_{video_key}", True)
                self.session.set(f"answering_{video_key}", False)
                st.rerun()

        with col2:
            if self.session.get(f"showing_{video_key}") and st.button("Done", key=f"stop_{video_key}"):
                self.session.set(f"answering_{video_key}", True)
                self.session.set(f"showing_{video_key}", False)
                st.rerun()

        if self.session.get(f"showing_{video_key}"):
            st.video(video_path)
            self.session_manager.start_session(video_key)

        st.caption("Please press 'Done' once you have watched the video.")

        if self.session.get(f"answering_{video_key}"):
            self.questionnaire_manager.show_video_questions(video_key)


    def show_news_step_2(self, article_key, article_path, is_positive=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Show me the article", key=f"start_{article_key}"):
                self.session.set(f"showing_{article_key}", True)
                self.session.set(f"answering_{article_key}", False)
                st.rerun()

        with col2:
            if self.session.get(f"showing_{article_key}") and st.button("Done", key=f"done_{article_key}"):
                self.session.set(f"answering_{article_key}", True)
                self.session.set(f"showing_{article_key}", False)
                st.rerun()

        if self.session.get(f"showing_{article_key}"):
            try:
                with open(article_path, "r", encoding="utf-8") as file:
                    article_text = file.read()
                    st.markdown(article_text)
            except FileNotFoundError:
                st.error("Article file not found. Please check the path.")
            self.session_manager.start_session(article_key)

        st.caption("Please press 'Done' once you have read the article.")

        if self.session.get(f"answering_{article_key}"):
            self.questionnaire_manager.show_news_questions(article_key, is_positive=is_positive)


    def show_voice_input_step(self, data_storage, voice_analyzer):
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
                    if saved_path is None:
                        st.error("Audio save failed: No path returned from save function.")
                    else:
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
