import requests
from datetime import datetime, timedelta
from . import token_store


GRAPH_URL = "https://graph.microsoft.com/v1.0/me/calendar/getSchedule"


def get_availability(emails, start, end):
    headers = {
        "Authorization": f"Bearer {token_store.ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "schedules": emails,
        "startTime": {
            "dateTime": start,
            "timeZone": "UTC"
        },
        "endTime": {
            "dateTime": end,
            "timeZone": "UTC"
        },
        "availabilityViewInterval": 30
    }

    response = requests.post(GRAPH_URL, headers=headers, json=body)
    return response.json()


def find_free_slots(schedule_data, start, end, duration_minutes):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    work_start_hour = 9
    work_end_hour = 18

    current = start_dt
    valid_slots = []

    # Extract busy intervals
    busy_blocks = []

    for user in schedule_data.get("value", []):
        for item in user.get("scheduleItems", []):
            busy_start = datetime.fromisoformat(item["start"]["dateTime"])
            busy_end = datetime.fromisoformat(item["end"]["dateTime"])
            busy_blocks.append((busy_start, busy_end))

    # Generate timeline
    while current + timedelta(minutes=duration_minutes) <= end_dt:

        # Skip weekends
        if current.weekday() < 5:

            # Restrict working hours
            if work_start_hour <= current.hour < work_end_hour:

                slot_end = current + timedelta(minutes=duration_minutes)

                conflict = False
                for busy_start, busy_end in busy_blocks:
                    if current < busy_end and slot_end > busy_start:
                        conflict = True
                        break

                if not conflict:
                    valid_slots.append(current.isoformat())

        current += timedelta(minutes=30)

    return valid_slots[:3]  # Return top 3 slots