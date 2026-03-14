# """
# Central API router for Luminara
# """

# from fastapi import APIRouter
# from api.agent_routes import router as agent_router

# # Create main router
# router = APIRouter()

# # Register agent routes
# router.include_router(agent_router, prefix="/agent")


# @router.get("/status")
# def system_status():
#     return {
#         "system": "Luminara Security Platform",
#         "status": "operational"
#     }

"""
Central API router for Luminara
"""

from fastapi import APIRouter
from api.agent_routes import router as agent_router

# Create main router
router = APIRouter()

# Health check
@router.get("/status")
def system_status():
    return {
        "system": "Luminara Security Platform",
        "status": "operational"
    }

# Register agent routes
router.include_router(agent_router, prefix="/agent")