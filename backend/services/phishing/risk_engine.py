"""
Risk scoring engine for phishing detection.
"""

class RiskEngine:
    def calculate_risk(
        self,
        ai_result: dict,
        features: dict,
        vt_result: dict = None,
        domain_age_signal: bool = False  # Add domain age signal here
    ):
        """
        Combine AI prediction, feature signals, VirusTotal reputation, and domain age signal.
        """

        score = 0.0

        # --- AI Model Score ---
        if ai_result["label"] == "phishing":
            score += ai_result["score"]

        # --- Feature Signals ---
        if features["urgency_language"]:
            score += 0.05

        if features["financial_terms"]:
            score += 0.05

        if features["credential_request"]:
            score += 0.07

        if features["suspicious_tld"]:
            score += 0.05

        if features["ip_based_url"]:
            score += 0.08

        # --- VirusTotal Reputation ---
        if vt_result:
            malicious = vt_result.get("malicious", 0)
            suspicious = vt_result.get("suspicious", 0)

            score += malicious * 0.02
            score += suspicious * 0.01

        # --- Domain Age Signal ---
        if domain_age_signal:
            score += 0.05  # Add weight for new domain signal (you can adjust this weight)

        # --- Normalize ---
        score = min(score, 1.0)

        return {
            "phishing_probability": round(score, 3)
        }