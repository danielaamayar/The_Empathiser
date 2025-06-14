from PIL import Image
import cv2
import torch
from facenet_pytorch import MTCNN
from transformers import AutoFeatureExtractor, AutoModelForImageClassification, AutoConfig

class EmotionDetector:
    def __init__(self, device="cpu"):
        self.device = torch.device(device)
        self.mtcnn = MTCNN(keep_all=False, device=self.device)
        self.extractor = AutoFeatureExtractor.from_pretrained("trpakov/vit-face-expression")
        self.model = AutoModelForImageClassification.from_pretrained("trpakov/vit-face-expression").to(self.device)
        self.id2label = AutoConfig.from_pretrained("trpakov/vit-face-expression").id2label

    def detect_emotion (self, frame):
        # Convert OpenCV BGR frame to RGB PIL image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        boxes, _ = self.mtcnn.detect(image)

        if boxes is not None and len(boxes) > 0:
            x1, y1, x2, y2 = map(int, boxes[0])
            face = image.crop((x1, y1, x2, y2))
            inputs = self.extractor(images=face, return_tensors="pt").to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)

            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1).detach().cpu().numpy()[0]
            class_probabilities = {self.id2label[i]: prob * 100 for i, prob in enumerate(probabilities)}

            return face, class_probabilities

        return None, None
