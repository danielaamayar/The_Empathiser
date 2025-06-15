from pathlib import Path

class ProjectPaths:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data_outputs"
        self.environmental_content_dir = self.base_dir / "environmental_content"
        self.video1_path = self.environmental_content_dir / "Garbage.mp4"
        self.video2_path = self.environmental_content_dir / "Playing_cows.mp4"  
        self.article1_path = self.environmental_content_dir / "Article_1.txt" 
        self.article2_path = self.environmental_content_dir  / "Article_2.txt"   

        self.create_directories()
    
    def create_directories(self):
        for dir_path in [self.data_dir, self.environmental_content_dir]:
            dir_path.mkdir(exist_ok=True)

