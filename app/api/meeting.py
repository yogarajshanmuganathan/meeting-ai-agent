from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.services.meeting_service import create_teams_meeting


router = APIRouter(prefix="/meeting", tags=["Meeting"])


class BookingRequest(BaseModel):
    subject: str
    start_time: str
    duration_minutes: int
    attendees: list[str]


@router.post("/book")
def book_meeting(data: BookingRequest):

    start_dt = datetime.fromisoformat(data.start_time)
    end_dt = start_dt + timedelta(minutes=data.duration_minutes)

    result = create_teams_meeting(
        data.subject,
        start_dt.isoformat(),
        end_dt.isoformat(),
        data.attendees
    )

    return result