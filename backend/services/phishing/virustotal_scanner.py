"""
VirusTotal URL scanning service for Luminara
"""

import base64
import requests
from core.config import settings


class VirusTotalScanner:
    """
    Scan URLs using VirusTotal threat intelligence API.
    """

    BASE_URL = "https://www.virustotal.com/api/v3"

    def __init__(self):
        self.api_key = settings.VIRUSTOTAL_API_KEY

        if not self.api_key:
            raise ValueError("VirusTotal API key not configured")

        self.headers = {
            "x-apikey": self.api_key
        }

    def _encode_url(self, url: str) -> str:
        """
        VirusTotal requires URL-safe base64 encoding for lookups.
        """
        encoded = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        return encoded

    def check_existing_report(self, url: str):
        """
        Check if VirusTotal already has analysis data for the URL.
        """

        encoded_url = self._encode_url(url)

        url_endpoint = f"{self.BASE_URL}/urls/{encoded_url}"

        try:
            response = requests.get(url_endpoint, headers=self.headers, timeout=10)

            if response.status_code == 200:
                stats = response.json()["data"]["attributes"]["last_analysis_stats"]
                return stats

        except requests.RequestException:
            pass

        return None

    def submit_url_for_scan(self, url: str):
        """
        Submit URL to VirusTotal for scanning.
        """

        endpoint = f"{self.BASE_URL}/urls"

        data = {"url": url}

        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                data=data,
                timeout=10
            )

            if response.status_code == 200:
                analysis_id = response.json()["data"]["id"]
                return analysis_id

        except requests.RequestException:
            pass

        return None

    def scan_url(self, url: str):
        """
        Main method used by phishing detection pipeline.
        """

        # Step 1 — Check existing report
        stats = self.check_existing_report(url)

        if stats:
            return stats

        # Step 2 — Submit for scanning
        analysis_id = self.submit_url_for_scan(url)

        if not analysis_id:
            return {"error": "Failed to submit URL"}

        # Step 3 — Retrieve analysis
        analysis_endpoint = f"{self.BASE_URL}/analyses/{analysis_id}"

        try:
            response = requests.get(
                analysis_endpoint,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                stats = response.json()["data"]["attributes"]["stats"]
                return stats

        except requests.RequestException:
            pass

        return {"error": "Analysis unavailable"}