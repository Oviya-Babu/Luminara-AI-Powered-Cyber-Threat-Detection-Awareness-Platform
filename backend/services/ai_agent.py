"""
AI Security Agent for Luminara.

This module decides which security system
should handle a user request.
"""

from typing import Dict


class AISecurityAgent:
    """
    Central intelligence of the Luminara system.
    Determines which module should process input.
    """

    def analyze_input(self, user_input: Dict) -> Dict:
        """
        Analyze user request and route it to the correct module.
        """

        input_type = user_input.get("type")

        if input_type == "text":
            return {
                "module": "phishing_detector",
                "message": "Routing to phishing detection system"
            }

        elif input_type == "media":
            return {
                "module": "deepfake_detector",
                "message": "Routing to deepfake detection system"
            }

        elif input_type == "learning":
            return {
                "module": "learning_system",
                "message": "Routing to cybersecurity learning module"
            }

        else:
            return {
                "module": "unknown",
                "message": "Unable to determine request type"
            }