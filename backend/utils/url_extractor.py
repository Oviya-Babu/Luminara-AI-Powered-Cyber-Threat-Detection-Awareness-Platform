"""
Utility for extracting URLs from text messages.
"""

import re


class URLExtractor:
    """
    Extract URLs from message text.
    """

    # Regex pattern to detect URLs
    URL_REGEX = r"(https?://[^\s]+|www\.[^\s]+)"

    @staticmethod
    def extract_urls(text: str):
        """
        Extract URLs from a given text message.
        """

        if not text:
            return []

        urls = re.findall(URLExtractor.URL_REGEX, text)

        return urls