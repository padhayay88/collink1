from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import time
from utils.match_logic_optimized import CollegePredictorOptimized

router = APIRouter(tags=["predictions"])

# Initialize the optimized predictor
predictor = CollegePredictorOptimized(load_essential_only=True)

class PredictionRequest(BaseModel):
    exam: str
    rank: int
    category: str = "General"
    gender: str = "All"
    quota: str = "All India"
    tolerance_percent: float = 0.0
    states: Optional[List[str]] = None
    load_full_data: bool = False
    limit: Optional[int] = 10000

class PredictionResponse(BaseModel):
    exam: str
    rank: int
    category: str
    predictions: List[dict]
    response_time: float
    data_source: str

@router.post("/predict", response_model=PredictionResponse)
async def predict_colleges(request: PredictionRequest):
    """
    Predict colleges based on exam rank and category
    """
    start_time = time.time()
    
    try:
        # Validate exam type
        valid_exams = ["jee", "neet", "ielts"]
        if request.exam.lower() not in valid_exams:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid exam type. Must be one of: {', '.join(valid_exams)}"
            )
        
        # Validate rank
        if request.rank <= 0:
            raise HTTPException(
                status_code=400, 
                detail="Rank must be a positive number"
            )
        
        # Get predictions using optimized predictor
        predictions = predictor.predict_colleges(
            exam=request.exam.lower(),
            rank=request.rank,
            category=request.category,
            gender=request.gender,
            quota=request.quota,
            tolerance_percent=request.tolerance_percent,
            states=request.states,
            load_full_data=request.load_full_data,
            limit=(request.limit or 10000)
        )
        
        response_time = time.time() - start_time
        
        # Determine data source
        data_status = predictor.get_data_status()
        data_source = data_status["data_loaded"].get(request.exam.lower(), "unknown")
        
        return PredictionResponse(
            exam=request.exam.lower(),
            rank=request.rank,
            category=request.category,
            predictions=predictions,
            response_time=response_time,
            data_source=data_source
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/data-status")
async def get_data_status():
    """Get current data loading status"""
    return predictor.get_data_status()

# --- Combined predictions (multi-exam) ---
class CombinedPredictionRequest(BaseModel):
    exams: List[str]
    rank: int
    category: str = "General"
    gender: str = "All"
    quota: str = "All India"
    tolerance_percent: float = 0.0
    states: Optional[List[str]] = None
    limit: Optional[int] = 10000


@router.post("/predict/combined")
async def predict_combined(request: CombinedPredictionRequest):
    """Run predictions across multiple exams and combine results with exam tags."""
    start_time = time.time()
    exams = [e.lower() for e in (request.exams or [])]
    valid = {"jee", "neet", "ielts"}
    exams = [e for e in exams if e in valid]
    if not exams:
        raise HTTPException(status_code=400, detail="No valid exams provided. Use any of: jee, neet, ielts")

    combined: List[dict] = []
    try:
        for exam in exams:
            preds = predictor.predict_colleges(
                exam=exam,
                rank=request.rank,
                category=request.category,
                gender=request.gender,
                quota=request.quota,
                tolerance_percent=request.tolerance_percent,
                states=request.states,
                load_full_data=False,
                limit=(request.limit or 10000),
            )
            for p in preds:
                p["exam"] = exam
            combined.extend(preds)

        response_time = time.time() - start_time
        return {
            "exams": exams,
            "rank": request.rank,
            "category": request.category,
            "predictions": combined,
            "response_time": response_time,
            "total": len(combined),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preload-data/{exam}")
async def preload_exam_data(exam: str):
    """Preload full data for a specific exam"""
    try:
        predictor.preload_full_data(exam)
        return {"message": f"Full data preloaded for {exam}", "status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error preloading data: {str(e)}"
        )

@router.get("/performance-test")
async def performance_test():
    """Test API performance with sample queries"""
    results = {}
    
    # Test JEE prediction
    start_time = time.time()
    jee_predictions = predictor.predict_colleges("jee", 100000, "General")
    jee_time = time.time() - start_time
    results["jee_100000"] = {"time": jee_time, "results": len(jee_predictions)}
    
    # Test NEET prediction
    start_time = time.time()
    neet_predictions = predictor.predict_colleges("neet", 20000, "General")
    neet_time = time.time() - start_time
    results["neet_20000"] = {"time": neet_time, "results": len(neet_predictions)}
    
    # Test IELTS prediction
    start_time = time.time()
    ielts_predictions = predictor.predict_colleges("ielts", 7, "General")
    ielts_time = time.time() - start_time
    results["ielts_7"] = {"time": ielts_time, "results": len(ielts_predictions)}
    
    return {
        "performance_test": results,
        "data_status": predictor.get_data_status()
    } 