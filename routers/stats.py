from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
async def get_stats():
    # Dummy stats data, replace with actual logic to fetch stats
    return {
        "neet": 1234,
        "jee": 2345,
        "pdf_universities": 345,
        "total": 3924
    }
