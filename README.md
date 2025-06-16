# The Empathiser

The Empathiser is a research tool designed to explore how different types of audiovisual and written environmental content trigger empathetic responses in users.

Powered by Streamlit, it combines facial expression recognition with voice sentiment analysis, enabling researchers to capture and analyse emotional reactions in real time.

## What It Does

- Detects facial expressions using MTCNN and ViT-Face-Expression (via Hugging Face).
- Records voice input and performs sentiment analysis.
- Presents a sequence of videos and news articles.
- Collects demographic and emotional data in a structured session flow.
- Stores and manages user responses securely.

## Tech Stack

- Frontend: Streamlit
- Face Detection: MTCNN (via PyTorch)
- Emotion Recognition: ViT-Face-Expression (Hugging Face Transformers)
- Voice Sentiment: RoBERTa model (Hugging Face)
- Utilities: OpenCV, NumPy, Matplotlib
- Session/Data Handling: Custom Python classes and file storage

## Setup Instructions
Clone this repository:

```bash
git clone https://github.com/your-username/the_empathiser.git
cd the_empathiser
```

Install required Python packages:

```
bash
pip install -r requirements.txt
```

🔗 Download Large Model Files
Some required transformer models are too large to be included in this repo.
Please download them from this SharePoint folder: https://artslondon-my.sharepoint.com/:f:/g/personal/d_amayarueda0220241_arts_ac_uk/Ei2xHrsRs5RBikI-UHMHMfMBWUtUCMgCq7tCQRZWTw9r0A?e=9MaJ4c 

*Interface Note*
The interface background colour has been customised to a light tone: 

```
st.markdown("""<style>.stApp {background-color: #F6F6EE;}</style>""", unsafe_allow_html=True)
```

If you're using dark mode this might cause visibility issues. Feel free to comment out or adjust this line if needed.

## Contact
If you have questions about the project or encounter issues, feel free to reach out: danielaamayar@gmail.com

