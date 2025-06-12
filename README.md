# The_Empathiser
A tool to determine what kind of audiovisual and text content triggers—or doesn't trigger—people's empathy.

The Empathiser tool uses the **PyTorch MTCNN** model for face detection and the **ViT-Face-Expression** model from Hugging Face for emotion recognition. It is built with **Streamlit** for the user interface and relies on common libraries like OpenCV, NumPy, and Matplotlib for video processing and visualization.

# Setup instructions:

1. **Install Miniconda or Anaconda**:
Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)

2. **Set Up the `ai4media` Environment**:

Download the [`ai4media_environment.yml`](https://git.arts.ac.uk/24003330/AI-4-Media-Project-Daniela-Amaya/blob/main/ai4media_environment.yml) file from this repository.

Create the environment:

```
conda env create -f ai4media_environment.yml
```
Activate the environment:
```
conda activate ai4media
```
All dependencies are listed in the `ai4media_environment.yml` file.

Or if you want yo can: 

```
conda activate ai4media
```
```
pip freeze > requirements.txt
```
```
pip install -r requirements.txt
```

Some transformer files are too large to include in the repository. Download them from this sharepoint folder: https://artslondon-my.sharepoint.com/:f:/g/personal/d_amayarueda0220241_arts_ac_uk/Ei2xHrsRs5RBikI-UHMHMfMBWUtUCMgCq7tCQRZWTw9r0A?e=9MaJ4c 

Disclaimer: I modified the interface's background colour, and it may not perform well in dark mode (e.g., at night). If needed, you can comment out the first line of code where the background colour is set.