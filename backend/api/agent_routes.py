from fastapi import APIRouter
from services.ai_agent import AISecurityAgent

router = APIRouter()

agent = AISecurityAgent()


@router.post("/analyze")
def analyze_request(request: dict):
    """
    Analyze user input and determine which module should process it.
    """
    result = agent.analyze_input(request)
    return result