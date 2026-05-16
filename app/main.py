# app/main.py

from fastapi import FastAPI

from app.routes.chat import (
    router as chat_router
)


app = FastAPI(
    title="SHL Assessment Recommender API",
    version="1.0.0"
)


# ====================================
# Health Endpoint
# ====================================

@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }


# ====================================
# Chat Routes
# ====================================

app.include_router(chat_router)


# ====================================
# Root Endpoint
# ====================================

@app.get("/")
def root():

    return {
        "message": (
            "SHL Assessment Recommender API is running"
        )
    }


# ====================================
# Vercel Handler
# ====================================

handler = app
