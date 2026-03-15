from fastapi import APIRouter
from services.phishing.phishing_detector import PhishingDetector

router = APIRouter()

detector = PhishingDetector()


@router.post("/analyze")
def analyze_message(data: dict):

    message = data.get("message", "")

    result = detector.analyze(message)

    return result