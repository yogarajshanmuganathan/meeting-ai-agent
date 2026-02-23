from fastapi import APIRouter
from pydantic import BaseModel
from app.services.schedule_service import get_availability, find_free_slots


router = APIRouter(prefix="/schedule", tags=["Schedule"])


class ScheduleRequest(BaseModel):
    emails: list[str]
    start: str
    end: str
    duration_minutes: int


@router.post("/optimize")
def optimize_schedule(data: ScheduleRequest):
    availability = get_availability(
        data.emails,
        data.start,
        data.end
    )

    slot = find_free_slots(
        availability,
        data.start,
        data.end,
        data.duration_minutes
    )

    if slot:
        return {"suggested_slots": slot}

    return {"message": "No common slot found"}