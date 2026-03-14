"""
Phishing Feature Extraction Engine
Used to detect social engineering patterns inside messages.
"""

import re
from urllib.parse import urlparse


class FeatureExtractor:
    """
    Extract phishing-related features from text.
    """

    # Common urgency signals used in phishing
    URGENCY_PATTERNS = [
        "urgent",
        "immediately",
        "act now",
        "verify now",
        "limited time",
        "suspended",
        "locked",
        "deadline",
        "expire",
        "final warning"
    ]

    # Financial context indicators
    FINANCIAL_PATTERNS = [
        "bank",
        "account",
        "payment",
        "transaction",
        "credit card",
        "debit",
        "invoice",
        "billing"
    ]

    # Credential harvesting attempts
    CREDENTIAL_PATTERNS = [
        "password",
        "login",
        "verify identity",
        "confirm account",
        "update credentials",
        "security check",
        "sign in"
    ]

    # Suspicious TLDs frequently used in phishing
    SUSPICIOUS_TLDS = [
        ".xyz",
        ".top",
        ".club",
        ".online",
        ".site",
        ".info"
    ]

    URL_REGEX = r"(https?://[^\s]+|www\.[^\s]+)"

    def __init__(self):
        pass

    def extract_urls(self, text: str):
        """
        Extract URLs from message text.
        """
        return re.findall(self.URL_REGEX, text)

    def detect_urgency(self, text: str):
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in self.URGENCY_PATTERNS)

    def detect_financial_terms(self, text: str):
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in self.FINANCIAL_PATTERNS)

    def detect_credential_request(self, text: str):
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in self.CREDENTIAL_PATTERNS)

    def detect_suspicious_tld(self, urls):
        """
        Detect suspicious top-level domains.
        """
        for url in urls:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            for tld in self.SUSPICIOUS_TLDS:
                if domain.endswith(tld):
                    return True

        return False

    def detect_ip_based_url(self, urls):
        """
        Detect URLs that use IP addresses instead of domain names.
        Example: http://192.168.1.1/login
        """
        ip_pattern = r"http[s]?://\d{1,3}(\.\d{1,3}){3}"

        for url in urls:
            if re.search(ip_pattern, url):
                return True

        return False

    def extract_features(self, text: str):
        """
        Main feature extraction method.
        """

        urls = self.extract_urls(text)

        features = {
            "has_url": len(urls) > 0,
            "num_urls": len(urls),
            "urgency_language": self.detect_urgency(text),
            "financial_terms": self.detect_financial_terms(text),
            "credential_request": self.detect_credential_request(text),
            "suspicious_tld": self.detect_suspicious_tld(urls),
            "ip_based_url": self.detect_ip_based_url(urls),
        }

        return features