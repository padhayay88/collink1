from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
import os
import json
from pathlib import Path
import requests
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
    per_college_limit: Optional[int] = 1
    ownership: Optional[str] = None  # "Any" | "Government" | "Private"

class PredictionResponse(BaseModel):
    exam: str
    rank: int
    category: str
    predictions: List[dict]
    response_time: float
    data_source: str


# --- AI Picks ---
class AIPicksRequest(BaseModel):
    exam: str
    rank: int
    category: str = "General"
    gender: str = "All"
    quota: str = "All India"
    tolerance_percent: float = 0.0
    states: Optional[List[str]] = None
    load_full_data: bool = False
    limit: Optional[int] = 50
    per_college_limit: Optional[int] = 1
    ownership: Optional[str] = None
    # Optional user preferences for AI ranking
    budget: Optional[int] = None
    interests: Optional[List[str]] = None
    goals: Optional[List[str]] = None

class AIPick(BaseModel):
    college: str
    branch: Optional[str] = None
    opening_rank: Optional[int] = None
    closing_rank: Optional[int] = None
    your_rank: int
    confidence_level: Optional[str] = None
    category: Optional[str] = None
    quota: Optional[str] = None
    location: Optional[str] = None
    ai_score: float
    match_reasons: List[str]

class AIPicksResponse(BaseModel):
    exam: str
    rank: int
    category: str
    total: int
    picks: List[AIPick]
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
        valid_exams = ["jee", "neet", "ielts", "cat"]
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
            limit=(request.limit or 10000),
            per_college_limit=(request.per_college_limit or 1),
            ownership=(request.ownership or None),
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
    ownership: Optional[str] = None


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
                ownership=(request.ownership or None),
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

def _compute_ai_score(base: Dict[str, Any], user_rank: int, states: Optional[List[str]] = None) -> (float, List[str]):
    """Lightweight AI score based on rank fit, confidence, and state preference.
    Returns a score in 0-100 and a list of match reasons.
    """
    reasons: List[str] = []
    score = 0.0

    closing = base.get("closing_rank") or 0
    opening = base.get("opening_rank") or closing or 0
    confidence_level = (base.get("confidence_level") or base.get("confidence") or "").lower()

    # Rank fit: better when user_rank <= closing_rank; scale by gap
    if closing and user_rank:
        gap = max(0, closing - user_rank)
        # Normalize by closing (cap influence)
        rank_fit = min(1.0, gap / max(1.0, closing))
        score += rank_fit * 60.0  # up to 60 pts
        if gap > 0:
            reasons.append("Your rank is within historical closing range")
        else:
            reasons.append("Near the closing rank range")

    # Confidence boost (from predictor)
    if confidence_level == "high":
        score += 20
        reasons.append("High confidence based on historical data")
    elif confidence_level == "medium":
        score += 10
        reasons.append("Moderate confidence from historical trends")

    # State preference match
    if states:
        loc = (base.get("location") or "").strip()
        cutoff_state = loc.split(",")[-1].strip() if "," in loc else loc
        if cutoff_state and cutoff_state in states:
            score += 10
            reasons.append(f"Matches preferred state: {cutoff_state}")

    # Category alignment (same category)
    if (base.get("category") or "").lower() == (base.get("user_category") or "").lower():
        score += 5
        reasons.append("Category alignment")

    # Quota alignment
    if (base.get("quota") or "All India") == "All India":
        score += 5
        reasons.append("All India quota availability")

    return max(0.0, min(100.0, score)), reasons


def _llm_generate_colleges(prompt: str) -> List[str]:
    """Query OpenAI or Google Gemini to get a list of college suggestions. Falls back to empty list."""
    # Try OpenAI first
    try:
        if os.getenv("OPENAI_API_KEY"):
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are an assistant helping with Indian college recommendations. Reply with a numbered list of colleges only."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            }
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=20,
            )
            r.raise_for_status()
            data = r.json()
            content = data["choices"][0]["message"]["content"]
            lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
            names: List[str] = []
            for ln in lines:
                # remove list numbers/bullets
                ln = ln.lstrip("-• ")
                ln = ln.split(".", 1)[-1].strip() if ln[:2].isdigit() else ln
                if ln:
                    names.append(ln)
            return names[:20]
    except Exception:
        pass

    # Try Google Gemini
    try:
        if os.getenv("GOOGLE_API_KEY"):
            model = "gemini-1.5-flash-latest"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={os.getenv('GOOGLE_API_KEY')}"
            contents = [
                {"role": "user", "parts": [{"text": "You are an assistant helping with Indian college recommendations. Reply with a numbered list of colleges only."}]},
                {"role": "user", "parts": [{"text": prompt}]},
            ]
            r = requests.post(url, json={"contents": contents}, timeout=20)
            r.raise_for_status()
            data = r.json()
            candidates = data.get("candidates", [])
            text = candidates[0]["content"]["parts"][0]["text"] if candidates else ""
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            names: List[str] = []
            for ln in lines:
                ln = ln.lstrip("-• ")
                ln = ln.split(".", 1)[-1].strip() if ln[:2].isdigit() else ln
                if ln:
                    names.append(ln)
            return names[:20]
    except Exception:
        pass

    return []


def _local_suggest_colleges(exam: str, states: Optional[List[str]], limit: int = 20) -> List[str]:
    """Use local datasets to suggest college names deterministically when LLM isn't available.
    Priority:
      1) data/{exam}_1000_cutoffs.json
      2) data/{exam}_cutoffs.json
      3) data/college_info_enhanced.json or data/college_info.json
    """
    names: List[str] = []

    def extract_state(loc: str) -> Optional[str]:
        if not loc:
            return None
        parts = [p.strip() for p in loc.split(",")]
        return parts[-1] if parts else None

    # Try cutoff-based files first
    for fname in [f"data/{exam}_1000_cutoffs.json", f"data/{exam}_cutoffs.json"]:
        p = Path(fname)
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Prefer distinct college names, optionally filter by state
                seen = set()
                for row in data:
                    college = row.get("college")
                    if not college:
                        continue
                    if states:
                        st = extract_state(row.get("location", ""))
                        if st and st not in states:
                            continue
                    if college not in seen:
                        seen.add(college)
                        names.append(college)
                        if len(names) >= limit:
                            return names
            except Exception:
                continue
    # Fallback to generic college info
    for fname in ["data/college_info_enhanced.json", "data/college_info.json"]:
        p = Path(fname)
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for row in data:
                    college = row.get("name")
                    if not college:
                        continue
                    if states:
                        st = extract_state(row.get("location", ""))
                        if st and st not in states:
                            continue
                    names.append(college)
                    if len(names) >= limit:
                        return names
            except Exception:
                continue
    return names[:limit]


def _norm_name(s: Optional[str]) -> str:
    try:
        return " ".join(((s or "").strip().lower()).split())
    except Exception:
        return (s or "").lower()


def _enrich_college_name_with_dataset(predictor: CollegePredictorOptimized, exam: str, name: str, user_rank: int) -> Optional[Dict[str, Any]]:
    """Find the closest matching cutoff row for a given college name and attach ranks/branch/location.
    Returns a dict shaped like base prediction rows or None if not found.
    """
    try:
        ex = (exam or "").lower()
        data = predictor.cutoff_data.get(ex) or []
        if not data:
            return None
        target = _norm_name(name)
        # First pass: contains match on normalized names
        candidates: List[Dict[str, Any]] = []
        for row in data:
            rc = row.get("college") or ""
            if not rc:
                continue
            rc_norm = _norm_name(rc)
            if target in rc_norm or rc_norm in target:
                candidates.append(row)
        # If no candidates, try loose token overlap (>=2 tokens)
        if not candidates:
            tks = set([t for t in target.split() if len(t) > 2])
            if tks:
                for row in data:
                    rc = row.get("college") or ""
                    rc_norm = _norm_name(rc)
                    rset = set([t for t in rc_norm.split() if len(t) > 2])
                    if len(tks.intersection(rset)) >= 2:
                        candidates.append(row)
        if not candidates:
            return None
        # Choose candidate whose closing_rank is nearest to user_rank
        def rank_gap(r):
            cr = r.get("closing_rank") or 0
            try:
                return abs(int(cr) - int(user_rank)) if cr else 10**9
            except Exception:
                return 10**9
        best = sorted(candidates, key=rank_gap)[0]
        # Build normalized prediction dict
        return {
            "college": best.get("college") or name,
            "branch": best.get("branch"),
            "opening_rank": best.get("opening_rank"),
            "closing_rank": best.get("closing_rank"),
            "your_rank": int(user_rank),
            "confidence_level": best.get("confidence_level") or best.get("confidence"),
            "category": best.get("category"),
            "quota": best.get("quota"),
            "location": best.get("location"),
        }
    except Exception:
        return None


def _default_colleges_for_exam(exam: str) -> List[str]:
    """Last-resort curated list to avoid empty screens."""
    exam = (exam or "").lower()
    if exam == "jee":
        return [
            "IIT Bombay", "IIT Delhi", "IIT Madras", "IIT Kanpur", "IIT Kharagpur",
            "IIT Roorkee", "IIT Guwahati", "IIT Hyderabad", "NIT Trichy", "NIT Surathkal",
            "NIT Warangal", "IIT BHU", "IIT (ISM) Dhanbad", "IIIT Hyderabad", "IIIT Bangalore",
        ]
    if exam == "neet":
        return [
            "AIIMS New Delhi", "AIIMS Jodhpur", "AIIMS Bhubaneswar", "AIIMS Bhopal", "AIIMS Rishikesh",
            "Maulana Azad Medical College", "Grant Medical College Mumbai", "KGMU Lucknow", "SMS Medical College Jaipur",
            "B.J. Medical College Ahmedabad", "Bangalore Medical College", "Madras Medical College",
        ]
    if exam == "ielts":
        return [
            "University of Toronto", "University of British Columbia", "McGill University", "University of Waterloo",
            "University of Alberta", "University of Calgary", "McMaster University",
        ]
    return ["College of Engineering", "National Institute of Technology", "Institute of Technology"]

@router.post("/predict/ai", response_model=AIPicksResponse)
async def predict_ai_picks(request: AIPicksRequest):
    """Return AI-ranked college picks based on rank and preferences."""
    start_time = time.time()
    try:
        if request.exam.lower() not in ["jee", "neet", "ielts"]:
            raise HTTPException(status_code=400, detail="Invalid exam type. Use jee, neet or ielts")

        # Get base predictions (broad set), then re-rank by AI score
        try:
            base_preds = predictor.predict_colleges(
                exam=request.exam.lower(),
                rank=request.rank,
                category=request.category,
                gender=request.gender,
                quota=request.quota,
                tolerance_percent=request.tolerance_percent,
                states=request.states,
                load_full_data=request.load_full_data,
                limit=max(200, request.limit or 50),  # fetch more, then rank
                per_college_limit=(request.per_college_limit or 1),
                ownership=(request.ownership or None),
            )
        except Exception as e:
            # Do not fail the endpoint; continue to LLM/local/curated fallbacks
            try:
                print(f"[AI Picks] predictor error: {e}")
            except Exception:
                pass
            base_preds = []

        # Apply adaptive proximity filters to prioritize near-rank results
        ex = request.exam.lower()
        near_w, far_w, very_far_w = 20000, 80000, 120000
        if ex == "neet":
            near_w = 60000 if request.rank >= 100000 else 50000
            far_w = 140000 if request.rank >= 100000 else 120000
            very_far_w = 250000
        else:
            if request.rank >= 100000:
                near_w, far_w, very_far_w = 50000, 120000, 200000

        def _within(item, w):
            closing = item.get("closing_rank") or 0
            return bool(closing) and abs(int(closing) - int(request.rank)) < int(w)

        filtered = [p for p in base_preds if _within(p, near_w)]
        if not filtered:
            filtered = [p for p in base_preds if _within(p, far_w)]
        if not filtered:
            filtered = [p for p in base_preds if _within(p, very_far_w)]
        if not filtered:
            filtered = base_preds  # as-is if nothing matches windows

        # Debug: log counts
        try:
            print(f"[AI Picks] exam={request.exam} rank={request.rank} cat={request.category} states={request.states} limit={request.limit} per_college_limit={request.per_college_limit}")
            print(f"[AI Picks] base_preds_count={len(base_preds)} filtered_count={len(filtered)} windows(near={near_w},far={far_w},vfar={very_far_w})")
        except Exception:
            pass

        picks: List[AIPick] = []
        for p in filtered:
            # Attach user category to help scoring
            p["user_category"] = request.category
            safe_rank = request.rank if isinstance(request.rank, (int, float)) and request.rank > 0 else (p.get("your_rank") or 1)
            ai_score, reasons = _compute_ai_score(p, int(safe_rank), request.states)
            picks.append(AIPick(
                college=p.get("college", "Unknown"),
                branch=p.get("branch"),
                opening_rank=p.get("opening_rank"),
                closing_rank=p.get("closing_rank"),
                your_rank=p.get("your_rank", request.rank),
                confidence_level=p.get("confidence_level") or p.get("confidence"),
                category=p.get("category"),
                quota=p.get("quota"),
                location=p.get("location"),
                ai_score=round(ai_score, 2),
                match_reasons=reasons,
            ))

        # If no base picks, use LLM fallback to suggest college names
        if not picks:
            prompt = (
                f"Suggest top colleges for exam={request.exam.upper()} for a candidate with rank={request.rank}, "
                f"category={request.category}. "
                f"States preference: {', '.join(request.states or []) or 'Any'}. "
                "Return a numbered list of college names only."
            )
            names = _llm_generate_colleges(prompt)
            if not names:
                # Deterministic local dataset fallback
                names = _local_suggest_colleges(request.exam.lower(), request.states, limit=max(10, request.limit or 20))
            if not names:
                # Final curated fallback
                names = _default_colleges_for_exam(request.exam.lower())[: max(10, request.limit or 20)]
            # Try to enrich each name with dataset match for ranks/branch/location
            enriched: List[Dict[str, Any]] = []
            for nm in names:
                row = _enrich_college_name_with_dataset(predictor, request.exam.lower(), nm, request.rank)
                if row:
                    enriched.append(row)
                else:
                    enriched.append({
                        "college": nm,
                        "branch": None,
                        "opening_rank": None,
                        "closing_rank": None,
                        "your_rank": request.rank,
                        "confidence_level": "medium",
                        "category": request.category,
                        "quota": request.quota,
                        "location": None,
                    })
            # Score enriched list
            for i, p in enumerate(enriched):
                p["user_category"] = request.category
                ai_score, reasons = _compute_ai_score(p, int(request.rank), request.states)
                if not reasons:
                    reasons = ["Suggested by AI model as strong fit for your rank"]
                picks.append(AIPick(
                    college=p.get("college", "Unknown"),
                    branch=p.get("branch"),
                    opening_rank=p.get("opening_rank"),
                    closing_rank=p.get("closing_rank"),
                    your_rank=p.get("your_rank", request.rank),
                    confidence_level=p.get("confidence_level") or p.get("confidence") or "medium",
                    category=p.get("category"),
                    quota=p.get("quota"),
                    location=p.get("location"),
                    ai_score=max(0.0, min(100.0, (72.0 - i) if ai_score == 0 else ai_score)),
                    match_reasons=reasons,
                ))

        # Sort by score desc and trim to limit
        picks.sort(key=lambda x: x.ai_score, reverse=True)
        limit = max(1, request.limit or 50)
        picks = picks[:limit]

        response_time = time.time() - start_time
        data_source = predictor.get_data_status()["data_loaded"].get(request.exam.lower(), "unknown")

        return AIPicksResponse(
            exam=request.exam.lower(),
            rank=request.rank,
            category=request.category,
            total=len(picks),
            picks=picks,
            response_time=response_time,
            data_source=data_source,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/predict/ai/diagnose")
async def ai_picks_diagnose(exam: str = "neet", states: Optional[str] = None, limit: int = 20):
    """Diagnostic: report data status, provider availability, and local suggestions.
    states: comma-separated list
    """
    ex = (exam or "neet").lower()
    st_list = [s.strip() for s in (states.split(",") if states else []) if s.strip()]
    status = predictor.get_data_status()
    data_loaded = status.get("data_loaded", {})

    # local suggestion sample
    local_sample = _local_suggest_colleges(ex, st_list, limit=max(5, limit))

    return {
        "exam": ex,
        "states": st_list,
        "limit": limit,
        "data_loaded": data_loaded,
        "llm_providers": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "google": bool(os.getenv("GOOGLE_API_KEY")),
        },
        "local_sample_count": len(local_sample),
        "local_sample": local_sample[:10],
    }
