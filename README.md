# The Empathiser

The Empathiser is a research tool designed to explore how different types of audiovisual and written environmental content trigger empathetic responses in users.

It combines facial expression recognition with voice sentiment analysis, enabling researchers to capture and analyse emotional reactions in real time.

## What It Does

- Detects facial expressions using MTCNN and ViT-Face-Expression (via Hugging Face).
- Records voice input and performs sentiment analysis.
- Presents a sequence of videos and news articles.
- Collects demographic and emotional data in a structured session flow.
- Stores and manages user responses.

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

## Download Large Model Files
Some required transformer models are too large to be included in this repo. Please download them from this [SharePoint folder](https://artslondon-my.sharepoint.com/my?id=%2Fpersonal%2Fd%5Famayarueda0220241%5Farts%5Fac%5Fuk%2FDocuments%2FFiles%20required%20AI%2D4%2Dmedia%20Project&ga=1).

## Running with Streamlit UI

Launch the interface using:

```
streamlit run streamlit_main.py
```

This will open the app in your default web browser.

## Data Outputs

Demographic data, self-report responses, facial emotion recognition, and sentiment analysis results are saved in each user’s folder inside the data_outputs folder.


## Disclaimers and Acknowledgements

This project was assisted by ChatGPT and Claude for debugging and implementing some specific functions, which are marked in the code.

The ```save_emotion_plot``` function was created by John Solomon Legara and originally published on [Medium](https://medium.com/@johnsolomonlegara/frame-by-frame-tracking-emotions-in-videos-with-ai-ee31a1a05ab6).

## Interface Note

The interface background colour has been customised to a light tone. If you're using dark mode, this might cause visibility issues. Feel free to comment out or adjust this line if needed.

```
st.markdown("""<style>.stApp {background-color: #F6F6EE;}</style>""", unsafe_allow_html=True)
```

## Contact

If you have questions about the project or encounter any issues, feel free to get in touch:
📧 danielaamayar@gmail.com

