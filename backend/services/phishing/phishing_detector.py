"""
Final PhishingDetector module for Luminara
Integrates:
- Feature Extraction
- AI Classifier
- URL Extraction
- VirusTotal Scan
- Domain Intelligence
- Risk Engine
"""

from services.phishing.feature_extractor import FeatureExtractor
from services.phishing.phishing_classifier import PhishingClassifier
from services.phishing.virustotal_scanner import VirusTotalScanner
from services.phishing.risk_engine import RiskEngine
from services.phishing.domain_intel import DomainIntel
from utils.url_extractor import URLExtractor


class PhishingDetector:

    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.classifier = PhishingClassifier()
        self.vt_scanner = VirusTotalScanner()
        self.domain_intel = DomainIntel()
        self.risk_engine = RiskEngine()

    def analyze(self, message: str):
        """
        Analyze a message for phishing probability.
        Returns structured output.
        """

        # --- Step 1: Extract Features ---
        features = self.feature_extractor.extract_features(message)

        # --- Step 2: AI Prediction ---
        ai_result = self.classifier.predict(message)

        # --- Step 3: Extract URLs ---
        urls = URLExtractor.extract_urls(message)

        vt_result = None
        domain_signal = False  # Initialize as False

        # --- Step 4: VirusTotal + Domain Intelligence ---
        if urls:
            # VirusTotal
            vt_result = self.vt_scanner.scan_url(urls[0])

            # Domain Intelligence
            domain_signal = self.domain_intel.is_new_domain(urls[0])

            # Add domain signal to features
            features["new_domain"] = domain_signal

        else:
            features["new_domain"] = False

        # --- Step 5: Risk Calculation ---
        risk = self.risk_engine.calculate_risk(
            ai_result=ai_result,
            features=features,
            vt_result=vt_result,
            domain_age_signal=domain_signal  # Pass the domain signal here
        )

        # --- Step 6: Return Complete Analysis ---
        return {
            "message": message,
            "ai_prediction": ai_result,
            "features": features,
            "virustotal": vt_result,
            "risk": risk
        }