# """
# Luminara Backend Entry Point
# """

# from fastapi import FastAPI
# from core.config import settings

# # Create FastAPI application
# app = FastAPI(
#     title=settings.APP_NAME,
#     version=settings.APP_VERSION,
#     description="AI Powered Cyber Threat Detection and Awareness Platform"
# )


# @app.get("/")
# def health_check():
#     """
#     Health check endpoint.
#     """
#     return {
#         "status": "running",
#         "application": settings.APP_NAME,
#         "version": settings.APP_VERSION
#     }


from fastapi import FastAPI
from core.config import settings
from api.router import router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Powered Cyber Threat Detection and Awareness Platform"
)

# Register API routes
app.include_router(router, prefix="/api")


@app.get("/")
def health_check():
    return {
        "status": "running",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION
    }