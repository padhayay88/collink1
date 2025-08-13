from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from pathlib import Path

# Import routers
from routers import predict, college, search
from routers import features

app = FastAPI(
    title="Collink - College Predictor API",
    description="API for predicting colleges based on competitive exam ranks (JEE, NEET, IELTS)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/api/v1", tags=["prediction"])
app.include_router(college.router, prefix="/api/v1", tags=["college"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(features.router, prefix="/api/v1", tags=["features"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Collink College Predictor API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/api/v1/predict",
            "college": "/api/v1/college/{college_name}",
            "search": "/api/v1/search?query={college_name}",
            "exams": "/api/v1/exams"
        }
    }

@app.get("/api/v1/exams")
async def get_exams():
    """Get list of supported exams"""
    return {
        "exams": [
            {
                "id": "jee",
                "name": "JEE Advanced",
                "description": "Joint Entrance Examination Advanced",
                "supported": True
            },
            {
                "id": "neet",
                "name": "NEET UG",
                "description": "National Eligibility cum Entrance Test",
                "supported": True
            },
            {
                "id": "ielts",
                "name": "IELTS",
                "description": "International English Language Testing System",
                "supported": True
            }
        ]
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "collink-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 