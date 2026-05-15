from fastapi import FastAPI
from app.routes.chat import router as chat_router

# Create FastAPI app
app = FastAPI(
    title="SHL Assessment Recommender API",
    version="1.0.0"
)

# Health check endpoint
@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }

# Include chat routes
app.include_router(chat_router)