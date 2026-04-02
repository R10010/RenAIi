import joblib
import os


class Emotional3DAvatar:
    def __init__(self, dataset_path: str = "data"):
        # ... previous code ...
        self.emotion_model = self._load_emotion_model()

    def _load_emotion_model(self):
        model_path = "ml_pipeline/models/emotion/model.pkl"
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            return None

    def detect_emotion(self, text: str, audio: np.ndarray = None) -> str:
        # Use ML model if available
        if self.emotion_model:
            # Extract features from text (e.g., using TF-IDF)
            # For simplicity, fallback to keywords
            pass
        # Keyword fallback
        text_lower = text.lower()
        if any(k in text_lower for k in ["happy", "love", "great"]):
            return "happy"
        if any(k in text_lower for k in ["sad", "miss", "unhappy"]):
            return "sad"
        if any(k in text_lower for k in ["angry", "mad"]):
            return "angry"
        return "neutral"
