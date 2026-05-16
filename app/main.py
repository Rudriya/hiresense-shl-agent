from fastapi import FastAPI

app = FastAPI(
    title="SHL Assessment Recommender API",
    version="1.0.0"
)


# ====================================
# Root Endpoint
# ====================================

@app.get("/")
def root():

    return {
        "message": "API running"
    }


# ====================================
# Health Endpoint
# ====================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# ====================================
# IMPORT CHAT ROUTES LAST
# IMPORTANT:
# prevents heavy ML loading
# during startup
# ====================================

from app.routes.chat import (
    router as chat_router
)

app.include_router(chat_router)
