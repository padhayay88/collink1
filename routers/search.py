from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from pathlib import Path
from difflib import SequenceMatcher

router = APIRouter()

class SearchResult(BaseModel):
    college_name: str
    match_score: float
    exam: str
    branch: str
    location: str

@router.get("/search")
async def search_colleges(
    query: str = Query(..., description="Search term for college name"),
    exam: Optional[str] = Query(None, description="Filter by exam (jee, neet, ielts)"),
    limit: int = Query(100, description="Maximum number of results")
):
    """
    Search colleges by name with fuzzy matching
    """
    try:
        if not query or len(query.strip()) < 2:
            raise HTTPException(
                status_code=400, 
                detail="Search query must be at least 2 characters long"
            )
        
        results = []
        query_lower = query.lower().strip()
        
        # Search in cutoff data files
        exam_files = ["jee", "neet", "ielts"] if not exam else [exam]
        
        for exam_type in exam_files:
            cutoff_file = f"data/{exam_type}_cutoffs.json"
            data_path = Path(cutoff_file)
            
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    cutoffs_data = json.load(f)
                
                # Search in this exam's data
                for cutoff in cutoffs_data:
                    college_name = cutoff["college"]
                    college_lower = college_name.lower()
                    
                    # Calculate similarity score
                    similarity = SequenceMatcher(None, query_lower, college_lower).ratio()
                    
                    # Check if query is in college name
                    if query_lower in college_lower or similarity > 0.3:
                        results.append({
                            "college_name": college_name,
                            "match_score": similarity,
                            "exam": exam_type,
                            "branch": cutoff.get("branch", "N/A"),
                            "location": cutoff.get("location", "N/A"),
                            "opening_rank": cutoff.get("opening_rank"),
                            "closing_rank": cutoff.get("closing_rank")
                        })
        
        # Sort by match score (highest first)
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Remove duplicates and limit results
        unique_results = []
        seen_colleges = set()
        
        for result in results:
            college_key = f"{result['college_name']}_{result['exam']}"
            if college_key not in seen_colleges and len(unique_results) < limit:
                unique_results.append(result)
                seen_colleges.add(college_key)
        
        return {
            "query": query,
            "results": unique_results,
            "total_found": len(unique_results),
            "exam_filter": exam
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/suggestions")
async def get_search_suggestions(
    query: str = Query(..., description="Partial search term"),
    limit: int = Query(20, description="Maximum number of suggestions")
):
    """
    Get search suggestions based on partial input
    """
    try:
        if not query or len(query.strip()) < 1:
            return {"suggestions": []}
        
        suggestions = set()
        query_lower = query.lower().strip()
        
        # Search in all exam data files
        exam_files = ["jee", "neet", "ielts"]
        
        for exam_type in exam_files:
            cutoff_file = f"data/{exam_type}_cutoffs.json"
            data_path = Path(cutoff_file)
            
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    cutoffs_data = json.load(f)
                
                for cutoff in cutoffs_data:
                    college_name = cutoff["college"]
                    college_lower = college_name.lower()
                    
                    if query_lower in college_lower:
                        suggestions.add(college_name)
                        
                        if len(suggestions) >= limit:
                            break
        
        return {
            "query": query,
            "suggestions": list(suggestions)[:limit]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/popular")
async def get_popular_colleges(exam: Optional[str] = None, limit: int = 50):
    """
    Get popular colleges based on search frequency or ranking
    """
    try:
        popular_colleges = []
        
        if exam:
            # Get popular colleges for specific exam
            cutoff_file = f"data/{exam}_cutoffs.json"
            data_path = Path(cutoff_file)
            
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    cutoffs_data = json.load(f)
                
                # Sort by closing rank (lower rank = more popular)
                sorted_cutoffs = sorted(
                    cutoffs_data, 
                    key=lambda x: x.get("closing_rank", float('inf'))
                )
                
                # Get unique colleges
                seen_colleges = set()
                for cutoff in sorted_cutoffs:
                    if cutoff["college"] not in seen_colleges and len(popular_colleges) < limit:
                        popular_colleges.append({
                            "name": cutoff["college"],
                            "exam": exam,
                            "best_rank": cutoff.get("closing_rank"),
                            "branch": cutoff.get("branch")
                        })
                        seen_colleges.add(cutoff["college"])
        else:
            # Get popular colleges across all exams
            all_colleges = {}
            
            for exam_type in ["jee", "neet", "ielts"]:
                cutoff_file = f"data/{exam_type}_cutoffs.json"
                data_path = Path(cutoff_file)
                
                if data_path.exists():
                    with open(data_path, 'r', encoding='utf-8') as f:
                        cutoffs_data = json.load(f)
                    
                    for cutoff in cutoffs_data:
                        college_name = cutoff["college"]
                        if college_name not in all_colleges:
                            all_colleges[college_name] = {
                                "name": college_name,
                                "exams": [],
                                "best_rank": float('inf')
                            }
                        
                        all_colleges[college_name]["exams"].append(exam_type)
                        rank = cutoff.get("closing_rank", float('inf'))
                        if rank < all_colleges[college_name]["best_rank"]:
                            all_colleges[college_name]["best_rank"] = rank
            
            # Sort by best rank and take top colleges
            popular_colleges = sorted(
                all_colleges.values(),
                key=lambda x: x["best_rank"]
            )[:limit]
        
        return {
            "popular_colleges": popular_colleges,
            "total": len(popular_colleges),
            "exam_filter": exam
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 