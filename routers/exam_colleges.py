from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
import pandas as pd
from pathlib import Path
import json

router = APIRouter()

# Load comprehensive college data
DATA_PATH = Path("comprehensive_colleges_list.csv")

@router.get("/api/colleges/exam/{exam_type}")
async def get_colleges_by_exam(
    exam_type: str,
    state: Optional[str] = None,
    min_rank: Optional[int] = None,
    max_rank: Optional[int] = None,
    category: Optional[str] = None,
    limit: int = 100
):
    """
    Get colleges by exam type (NEET/JEE) with optional filters
    """
    try:
        # Validate exam type
        exam_type = exam_type.upper()
        if exam_type not in ["NEET", "JEE"]:
            raise HTTPException(status_code=400, detail="Invalid exam type. Must be 'NEET' or 'JEE'")
        
        # Read the CSV file
        df = pd.read_csv(DATA_PATH)
        
        # Filter by exam type
        df = df[df['Exam Type'].str.upper() == exam_type]
        
        # Apply filters
        if state:
            df = df[df['State/UT'].str.lower() == state.lower()]
            
        if category:
            df = df[df['Category'].str.lower() == category.lower()]
            
        if min_rank is not None:
            # Extract max rank from range string (e.g., "100-200" -> 200)
            df = df[df['Ranking'].str.extract(r'(\d+)', expand=False).astype(float) >= min_rank]
            
        if max_rank is not None:
            # Extract min rank from range string (e.g., "100-200" -> 100)
            df = df[df['Ranking'].str.extract(r'(\d+)', expand=False).astype(float) <= max_rank]
        
        # Sort by ranking
        df = df.sort_values('Ranking')
        
        # Apply limit
        if limit > 0:
            df = df.head(limit)
            
        return df.to_dict(orient='records')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/colleges/stats/{exam_type}")
async def get_exam_stats(exam_type: str):
    """
    Get statistics for NEET/JEE colleges
    """
    try:
        exam_type = exam_type.upper()
        if exam_type not in ["NEET", "JEE"]:
            raise HTTPException(status_code=400, detail="Invalid exam type. Must be 'NEET' or 'JEE'")
            
        df = pd.read_csv(DATA_PATH)
        df = df[df['Exam Type'].str.upper() == exam_type]
        
        # Basic stats
        total_colleges = len(df)
        states = df['State/UT'].unique().tolist()
        categories = df['Category'].unique().tolist()
        
        # Top 10 colleges
        top_colleges = df.sort_values('Ranking').head(10).to_dict(orient='records')
        
        # State distribution
        state_dist = df['State/UT'].value_counts().to_dict()
        
        return {
            "total_colleges": total_colleges,
            "states": states,
            "categories": categories,
            "top_colleges": top_colleges,
            "state_distribution": state_dist
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
