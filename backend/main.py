from fastapi import FastAPI
from api.router import router as api_router

app = FastAPI(
    title="Luminara Cybersecurity API",
    description="AI-powered cyber threat detection and awareness platform",
    version="1.0"
)

# Include all routes from central router
app.include_router(api_router, prefix="/api")