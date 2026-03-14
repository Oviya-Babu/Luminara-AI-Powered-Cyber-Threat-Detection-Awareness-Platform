"""
Central API router for Luminara
"""

from fastapi import APIRouter
from api.agent_routes import router as agent_router
from api.phishing_routes import router as phishing_router

# --- Step 1: Create the main router ---
router = APIRouter()

# --- Step 2: Health check ---
@router.get("/status")
def system_status():
    return {
        "system": "Luminara Security Platform",
        "status": "operational",
        "version": "1.0"
    }

# --- Step 3: Register other routers ---

# Agent routes
router.include_router(agent_router, prefix="/agent")

# Phishing detection routes
router.include_router(phishing_router, prefix="/phishing")