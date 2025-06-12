class EmotionColors:
    
    angry: str = "red"
    disgust: str = "green"
    fear: str = "gray"
    happy: str = "yellow"
    neutral: str = "purple"
    sad: str = "blue"
    surprise: str = "orange"
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "angry": self.angry,
            "disgust": self.disgust,
            "fear": self.fear,
            "happy": self.happy,
            "neutral": self.neutral,
            "sad": self.sad,
            "surprise": self.surprise
        }
