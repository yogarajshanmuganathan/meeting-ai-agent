from fastapi import FastAPI

from app.api.schedule import router as schedule_router
from app.api.summarize import router as summarize_router
from app.api.auth import router as auth_router   # <-- THIS LINE MUST EXIST
from app.api.calendar import router as calendar_router
from app.api.meeting import router as meeting_router

app = FastAPI(title="AI Meeting Intelligence Agent")

app.include_router(schedule_router)
app.include_router(summarize_router)
app.include_router(auth_router)   # <-- THIS LINE MUST EXIST

app.include_router(calendar_router)
app.include_router(meeting_router)

@app.get("/")
def root():
    return {"status": "running"}