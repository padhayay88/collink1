from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import os
import requests

from utils.match_logic import CollegePredictor

router = APIRouter()


class TrendPoint(BaseModel):
    year: int
    opening_rank: Optional[int] = None
    closing_rank: Optional[int] = None


@router.get("/trends")
async def get_rank_trends(college: str, exam: str = "jee", years: int = 5):
    """Return cutoff rank trends for the past N years for a college.
    Falls back to synthetic trends when historical data is unavailable.
    """
    try:
        college_lower = college.lower()
        points: List[TrendPoint] = []

        # Prefer extended dataset when available
        extended_path = Path(f"data/{exam}_cutoffs_extended.json")
        normal_path = Path(f"data/{exam}_cutoffs.json")

        if extended_path.exists():
            with open(extended_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Expect entries with year fields
            filtered = [d for d in data if college_lower in d.get("college", "").lower()]
            years_seen = sorted({d.get("year") for d in filtered if d.get("year")}, reverse=True)[:years]
            for y in sorted(years_seen):
                year_entries = [d for d in filtered if d.get("year") == y]
                if not year_entries:
                    continue
                opening = min(e.get("opening_rank") for e in year_entries if e.get("opening_rank") is not None)
                closing = max(e.get("closing_rank") for e in year_entries if e.get("closing_rank") is not None)
                points.append(TrendPoint(year=int(y), opening_rank=opening, closing_rank=closing))
        elif normal_path.exists():
            with open(normal_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            filtered = [d for d in data if college_lower in d.get("college", "").lower()]
            if filtered:
                # Create synthetic trend around the observed closing ranks
                base_closing = int(sum(d.get("closing_rank", 0) for d in filtered) / max(1, len(filtered)))
                base_opening = int(sum(d.get("opening_rank", base_closing)) / max(1, len(filtered)))
                current_year = 2024
                for i in range(years):
                    # simulate slight improvement over years
                    factor = 1.0 - (years - i - 1) * 0.03
                    points.append(
                        TrendPoint(
                            year=current_year - (years - i - 1),
                            opening_rank=max(1, int(base_opening * factor)),
                            closing_rank=max(1, int(base_closing * factor)),
                        )
                    )

        if not points:
            raise HTTPException(status_code=404, detail="No trend data available for the requested college")

        return {"college": college, "exam": exam, "trends": [p.dict() for p in sorted(points, key=lambda p: p.year)]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AISummaryRequest(BaseModel):
    college_name: str


@router.post("/ai/summary")
async def ai_summary(req: AISummaryRequest):
    """Return an auto-generated pros/cons and summary for a college using local data.
    This does not call external services and works offline.
    """
    try:
        path = Path("data/college_info_enhanced.json")
        if not path.exists():
            path = Path("data/college_info.json")
        if not path.exists():
            raise HTTPException(status_code=404, detail="College data not found")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        target = None
        for c in data:
            if req.college_name.lower() in c.get("name", "").lower():
                target = c
                break
        if not target:
            raise HTTPException(status_code=404, detail="College not found")

        overview = target.get("overview") or f"{target.get('name')} is a reputed institution offering various programs."
        pros = target.get("pros") or ["Good placements", "Experienced faculty", "Strong alumni network"]
        cons = target.get("cons") or ["Highly competitive admissions", "Limited seats"]

        # Heuristic summary from available data
        summary = (
            f"{target.get('name')} in {target.get('location', 'India')} is known for {', '.join(pros[:2])}. "
            f"It offers programs such as {', '.join((target.get('courses_offered') or [])[:3])}. "
            f"Consider that {', '.join(cons[:1])}."
        )
        return {"name": target.get("name"), "overview": overview, "pros": pros, "cons": cons, "summary": summary}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class FuturePredictionRequest(BaseModel):
    exam: str
    current_rank: int
    mock_test_scores: Optional[List[int]] = None
    category: str = "General"
    gender: str = "All"
    quota: str = "All India"


@router.post("/predict/future")
async def predict_future_college(req: FuturePredictionRequest):
    """Estimate potential colleges by projecting rank improvement using mock scores.
    Simplified heuristic: average mock score improvement maps to rank reduction.
    """
    try:
        projected_rank = req.current_rank
        if req.mock_test_scores:
            avg = sum(req.mock_test_scores) / max(1, len(req.mock_test_scores))
            # Normalize assumed mock score out of 100 to an improvement factor
            improvement = max(0.0, min(0.3, (avg - 60) / 200))  # up to 30% better
            projected_rank = max(1, int(req.current_rank * (1 - improvement)))

        predictor = CollegePredictor()
        predictions = predictor.predict_colleges(
            exam=req.exam.lower(),
            rank=projected_rank,
            category=req.category,
            gender=req.gender,
            quota=req.quota,
        )

        return {
            "exam": req.exam,
            "current_rank": req.current_rank,
            "projected_rank": projected_rank,
            "predictions": predictions,
            "total_colleges": len(predictions),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Live seat availability (stub) ---
class SeatAvailabilityRequest(BaseModel):
    exam: str
    colleges: Optional[List[str]] = None
    state: Optional[str] = None


@router.get("/live-seats")
async def get_live_seats(exam: str = "jee", state: Optional[str] = None) -> Dict[str, Any]:
    """Stub endpoint for live seat availability. Returns static structure for now."""
    try:
        # Placeholder structure; integrate real sources later
        return {
            "exam": exam,
            "state": state,
            "last_updated": "just now",
            "sources": ["josaa", "mcc"],
            "colleges": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Gamification System ---
class UserProgress(BaseModel):
    user_id: str
    points: int = 0
    level: int = 1
    badges: List[str] = []
    achievements: List[str] = []


@router.get("/gamification/{user_id}")
async def get_user_progress(user_id: str) -> Dict[str, Any]:
    """Get user's gamification progress and achievements."""
    try:
        storage = Path("data/user_progress.json")
        if not storage.exists():
            # Create default progress for new user
            default_progress = {
                "user_id": user_id,
                "points": 0,
                "level": 1,
                "badges": ["New Explorer"],
                "achievements": ["First Visit"]
            }
            storage.write_text(json.dumps(default_progress, indent=2), encoding="utf-8")
            return default_progress
        
        data = json.loads(storage.read_text(encoding="utf-8"))
        user_data = data.get(user_id, {
            "user_id": user_id,
            "points": 0,
            "level": 1,
            "badges": ["New Explorer"],
            "achievements": ["First Visit"]
        })
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gamification/{user_id}/earn")
async def earn_points(user_id: str, action: str = "prediction", points: int = 10):
    """Earn points for user actions."""
    try:
        storage = Path("data/user_progress.json")
        data = {}
        if storage.exists():
            data = json.loads(storage.read_text(encoding="utf-8"))
        
        if user_id not in data:
            data[user_id] = {
                "user_id": user_id,
                "points": 0,
                "level": 1,
                "badges": ["New Explorer"],
                "achievements": ["First Visit"]
            }
        
        user_data = data[user_id]
        user_data["points"] += points
        
        # Level up logic
        new_level = (user_data["points"] // 100) + 1
        if new_level > user_data["level"]:
            user_data["level"] = new_level
            user_data["achievements"].append(f"Level {new_level} Reached!")
        
        # Badge logic
        if user_data["points"] >= 50 and "Active Learner" not in user_data["badges"]:
            user_data["badges"].append("Active Learner")
        if user_data["points"] >= 200 and "College Expert" not in user_data["badges"]:
            user_data["badges"].append("College Expert")
        
        storage.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return {"status": "success", "points_earned": points, "total_points": user_data["points"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SaveRequest(BaseModel):
    user_id: str
    college: str


@router.post("/saves")
async def save_college(req: SaveRequest):
    try:
        storage = Path("data/user_saves.json")
        saves: Dict[str, List[str]] = {}
        if storage.exists():
            saves = json.loads(storage.read_text(encoding="utf-8"))
        user_list = set(saves.get(req.user_id, []))
        user_list.add(req.college)
        saves[req.user_id] = sorted(user_list)
        storage.write_text(json.dumps(saves, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": "saved", "user_id": req.user_id, "colleges": saves[req.user_id]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/saves")
async def list_saves(user_id: str):
    storage = Path("data/user_saves.json")
    if not storage.exists():
        return {"user_id": user_id, "colleges": []}
    saves = json.loads(storage.read_text(encoding="utf-8"))
    return {"user_id": user_id, "colleges": saves.get(user_id, [])}


class CompareRequest(BaseModel):
    colleges: List[str]


@router.post("/compare")
async def compare_colleges(req: CompareRequest):
    try:
        path = Path("data/college_info_enhanced.json")
        if not path.exists():
            path = Path("data/college_info.json")
        if not path.exists():
            raise HTTPException(status_code=404, detail="College data not found")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        result = []
        for name in req.colleges:
            match = next((c for c in data if name.lower() in c.get("name", "").lower()), None)
            if match:
                result.append({
                    "name": match.get("name"),
                    "location": match.get("location"),
                    "nirf_rank": match.get("nirf_rank"),
                    "fees": (match.get("fees") or {}).get("total_annual"),
                    "average_package": (match.get("placement_stats") or {}).get("average_package"),
                    "overall_rating": (match.get("ratings") or {}).get("overall"),
                })
        return {"colleges": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AlertSubscribeRequest(BaseModel):
    email: str
    exam: str = "jee"


@router.post("/alerts/subscribe")
async def subscribe_alerts(req: AlertSubscribeRequest):
    try:
        storage = Path("data/alerts.json")
        alerts: List[Dict[str, str]] = []
        if storage.exists():
            alerts = json.loads(storage.read_text(encoding="utf-8"))
        # prevent duplicates
        exists = any(a["email"].lower() == req.email.lower() and a["exam"] == req.exam for a in alerts)
        if not exists:
            alerts.append({"email": req.email, "exam": req.exam})
            storage.write_text(json.dumps(alerts, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": "subscribed", "email": req.email, "exam": req.exam}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def list_alerts():
    storage = Path("data/alerts.json")
    if not storage.exists():
        return {"alerts": []}
    alerts = json.loads(storage.read_text(encoding="utf-8"))
    return {"alerts": alerts}


# ---- AI Chat (LLM-backed with fallbacks) ----
class ChatMessage(BaseModel):
    role: str  # "system" | "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    provider: Optional[str] = None  # "openai" | "google" | "local"
    model: Optional[str] = None


@router.post("/ai/chat")
async def ai_chat(req: ChatRequest):
    """
    Simple chat endpoint:
    - provider=openai: uses OpenAI Chat Completions (via REST)
    - provider=google: uses Gemini generateContent
    - default: local heuristic summary using available college data
    Environment variables:
      - OPENAI_API_KEY (for provider=openai)
      - GOOGLE_API_KEY (for provider=google)
    """
    try:
        provider = (req.provider or "local").lower()
        # Ensure we always include a brief system instruction for domain safety
        messages = req.messages or []
        if not messages or messages[0].role != "system":
            messages = [
                ChatMessage(role="system", content="You are a helpful assistant for college search in India. Be concise."),
                *messages,
            ]

        # Load few-shot examples (user-provided training data)
        examples_path = Path("data/ai_examples.json")
        few_shots: List[Dict[str, str]] = []
        if examples_path.exists():
            try:
                few_shots = json.loads(examples_path.read_text(encoding="utf-8"))[:6]
            except Exception:
                few_shots = []
        # Convert examples into message pairs and prepend after system
        if few_shots:
            example_msgs: List[ChatMessage] = []
            for ex in few_shots:
                q = ex.get("question")
                a = ex.get("answer")
                if q and a:
                    example_msgs.append(ChatMessage(role="user", content=q))
                    example_msgs.append(ChatMessage(role="assistant", content=a))
            # Insert examples after the first system message
            if example_msgs:
                messages = [messages[0], *example_msgs, *messages[1:]]

        if provider == "openai" and os.getenv("OPENAI_API_KEY"):
            try:
                payload = {
                    "model": req.model or "gpt-4o-mini",
                    "messages": [m.dict() for m in messages],
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
                return {"provider": "openai", "content": content}
            except Exception as e:
                # Fall through to local
                pass

        if provider == "google" and os.getenv("GOOGLE_API_KEY"):
            try:
                model = req.model or "gemini-1.5-flash-latest"
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={os.getenv('GOOGLE_API_KEY')}"
                # Convert messages to Gemini parts
                contents = []
                for m in messages:
                    contents.append({"role": m.role, "parts": [{"text": m.content}]})
                payload = {"contents": contents}
                r = requests.post(url, json=payload, timeout=20)
                r.raise_for_status()
                data = r.json()
                candidates = data.get("candidates", [])
                content = candidates[0]["content"]["parts"][0]["text"] if candidates else ""
                return {"provider": "google", "content": content}
            except Exception:
                # Fall through to local
                pass

        # Local heuristic: answer by searching known data files for college names and composing a response
        user_text = "\n".join(m.content for m in messages if m.role == "user")
        data_paths = [
            Path("data/college_info_enhanced.json"),
            Path("data/college_info.json"),
        ]
        snippets = []
        for p in data_paths:
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    for c in data[:80]:  # limit for speed
                        name = c.get("name", "")
                        if name and name.lower() in user_text.lower():
                            loc = c.get("location", "India")
                            rank = c.get("nirf_rank")
                            overview = (c.get("overview") or "")[:220]
                            snippets.append(f"- {name} ({loc}) NIRF: {rank or 'NA'}\n  {overview}")
                except Exception:
                    continue
        if not snippets:
            content = (
                "I can help with college suggestions, state-wise lists, ranks, and fees. "
                "Ask about a college or your rank, or use the Predict page for results."
            )
        else:
            content = "Here are some details based on your query:\n" + "\n".join(snippets[:5])
        return {"provider": "local", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Simple endpoint to "train" the local AI with custom Q&A examples ---
class TeachRequest(BaseModel):
    question: str
    answer: str


@router.post("/ai/teach")
async def ai_teach(req: TeachRequest):
    """Append a Q&A example used as few-shot guidance in future chats.
    Stored locally in data/ai_examples.json.
    """
    try:
        examples_path = Path("data/ai_examples.json")
        examples: List[Dict[str, str]] = []
        if examples_path.exists():
            try:
                examples = json.loads(examples_path.read_text(encoding="utf-8"))
            except Exception:
                examples = []
        # Deduplicate by exact question text
        if not any(e.get("question") == req.question for e in examples):
            examples.insert(0, {"question": req.question, "answer": req.answer})
        # Keep a reasonable cap
        examples = examples[:200]
        examples_path.write_text(json.dumps(examples, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": "ok", "stored": len(examples)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

