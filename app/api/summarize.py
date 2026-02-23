from fastapi import APIRouter

router = APIRouter(prefix="/summarize", tags=["Summarization"])

@router.post("/")
def summarize(payload: dict):
    return {
        "message": "Summarization endpoint working",
        "input": payload
    }