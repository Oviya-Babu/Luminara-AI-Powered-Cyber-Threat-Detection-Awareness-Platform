"""
Phishing Detection Engine for Luminara
"""

import re


class PhishingDetector:
    """
    Detect phishing indicators in text messages.
    """

    def __init__(self):
        """
        Initialize phishing keyword database.
        """

        self.phishing_keywords = [
            "verify immediately",
            "account suspended",
            "urgent action required",
            "click this link",
            "confirm your identity",
            "bank account locked",
            "update payment information",
            "security alert",
            "reset your password",
            "unusual activity detected"
        ]

    def detect_keywords(self, text: str):
        """
        Detect suspicious phishing keywords in text.
        """

        detected = []

        for keyword in self.phishing_keywords:
            if keyword in text.lower():
                detected.append(keyword)

        return detected

    def analyze_message(self, text: str):
        """
        Analyze text for phishing indicators and calculate risk score.
        """

        indicators = self.detect_keywords(text)

        risk_score = len(indicators) * 20

        if risk_score > 100:
            risk_score = 100

        return {
            "message": text,
            "risk_score": risk_score,
            "indicators": indicators
        }