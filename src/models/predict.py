"""
Module: predict.py
Lifecycle Stage 7: Model Testing & Inference Engine
Provides both programmatic prediction with confidence scoring
and interactive CLI testing as outlined in Stage 7 of the build guide.
"""

import os
import joblib
import numpy as np
from src.data.preprocess import clean_text


class NewsClassifier:
    """
    Production-ready news classifier class encapsulating model loading,
    text preprocessing, inference, and calibrated confidence calculation.
    """
    def __init__(self, model_path: str = "models/news_model.pkl", vectorizer_path: str = "models/tfidf_vectorizer.pkl"):
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            raise FileNotFoundError("Model or Vectorizer artifact not found. Please train model first.")
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.classes = list(self.model.classes_)

    def _softmax(self, x):
        """Softmax function with numerical stability."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=-1, keepdims=True)

    def predict(self, text: str) -> dict:
        """
        Classifies a single news article or headline string.
        Returns:
            {
                "category": str,
                "confidence": float,
                "cleaned_text": str,
                "category_scores": dict
            }
        """
        cleaned = clean_text(text)
        if not cleaned:
            return {
                "category": "unknown",
                "confidence": 0.0,
                "cleaned_text": "",
                "category_scores": {}
            }

        X = self.vectorizer.transform([cleaned])
        pred_label = self.model.predict(X)[0]

        # Decision function values mapped via softmax for calibrated relative confidence
        decision_scores = self.model.decision_function(X)[0]
        probs = self._softmax(decision_scores)
        pred_idx = self.classes.index(pred_label)
        confidence = float(probs[pred_idx])

        category_scores = {
            self.classes[i]: round(float(probs[i]), 4)
            for i in range(len(self.classes))
        }

        return {
            "category": pred_label,
            "confidence": round(confidence, 4),
            "cleaned_text": cleaned,
            "category_scores": category_scores
        }

    def batch_predict(self, texts: list) -> list:
        """Classifies a list of text strings efficiently."""
        return [self.predict(t) for t in texts]


def interactive_cli():
    """Interactive loop for manual CLI testing as required by the guide."""
    print("=" * 60)
    print("Stage 7: Interactive News Classifier CLI")
    print("Enter news headline or article to test. Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    classifier = NewsClassifier()

    while True:
        try:
            text = input("\nEnter News: ").strip()
            if not text:
                continue
            if text.lower() in ("exit", "quit", "q"):
                print("Exiting interactive testing.")
                break

            result = classifier.predict(text)
            print(f"\n>> PREDICTION : [{result['category'].upper()}]")
            print(f"   Confidence : {result['confidence'] * 100:.1f}%")
            print(f"   Cleaned    : '{result['cleaned_text']}'")
            print("   Top Probabilities:")
            top3 = sorted(result["category_scores"].items(), key=lambda x: x[1], reverse=True)[:3]
            for cat, score in top3:
                print(f"     * {cat:15s}: {score * 100:5.1f}%")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break


if __name__ == "__main__":
    interactive_cli()
