from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

enconded_response = tokenizer(transcription, return_tensors='pt')
sentiment_analysis = model(**encoded_response)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
scores_dict = {
    ¨negative¨: scores[0],
    ¨neutral¨: scores[1],
    ¨positive¨: scores[2]
}

print(scores_dict)
