"""
Domain intelligence for phishing detection
"""

import whois
from datetime import datetime


class DomainIntel:

    def __init__(self):
        pass

    def get_domain_age_days(self, url: str):
        """
        Returns the domain age in days.
        """

        try:
            domain_info = whois.whois(url)
            creation_date = domain_info.creation_date

            # Sometimes creation_date is a list
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if creation_date is None:
                return None

            delta = datetime.now() - creation_date
            return delta.days

        except Exception:
            return None

    def is_new_domain(self, url: str, threshold_days=30):
        """
        Returns True if domain is younger than threshold.
        """
        age_days = self.get_domain_age_days(url)
        if age_days is None:
            return False

        return age_days < threshold_days