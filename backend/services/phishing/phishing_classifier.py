"""
AI Phishing Classifier using Transformer models
"""

from transformers import pipeline


# Load model only once when server starts
classifier_pipeline = pipeline(
    "text-classification",
    model="ealvaradob/bert-finetuned-phishing"
)


class PhishingClassifier:

    def predict(self, text: str):

        if not text or len(text.strip()) == 0:
            return {
                "label": "unknown",
                "score": 0.0
            }

        result = classifier_pipeline(text)[0]

        return {
            "label": result["label"],
            "score": float(result["score"])
        }