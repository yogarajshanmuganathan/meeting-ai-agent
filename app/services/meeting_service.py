import requests
import uuid
from . import token_store
from app.db.database import get_db_connection

GRAPH_URL = "https://graph.microsoft.com/v1.0/me/events"


def generate_mock_teams_link():
    meeting_id = uuid.uuid4()
    return f"https://teams.microsoft.com/l/meetup-join/{meeting_id}"


def save_meeting_to_db(event_id, subject, start_time, duration, join_url, organizer_email):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO meetings (event_id, subject, start_time, duration_minutes, join_url, organizer_email)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    cursor.execute(insert_query, (
        event_id,
        subject,
        start_time,
        duration,
        join_url,
        organizer_email
    ))

    conn.commit()
    cursor.close()
    conn.close()


def create_teams_meeting(subject, start_time, end_time, attendees):
    headers = {
        "Authorization": f"Bearer {token_store.ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    join_url = generate_mock_teams_link()

    attendees_payload = [
        {
            "emailAddress": {
                "address": email,
                "name": email
            },
            "type": "required"
        }
        for email in attendees
    ]

    body = {
        "subject": subject,
        "start": {
            "dateTime": start_time,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "UTC"
        },
        "attendees": attendees_payload,
        "body": {
            "contentType": "HTML",
            "content": f"""
                <p><strong>Enterprise AI Meeting</strong></p>
                <p>Join here:</p>
                <p><a href='{join_url}'>{join_url}</a></p>
            """
        }
    }

    response = requests.post(GRAPH_URL, headers=headers, json=body)
    response_json = response.json()
    
    return {
        "event_id": response_json.get("id"),
        "subject": subject,
        "start_time": start_time,
        "join_url": join_url,
        "web_link": response_json.get("webLink")
    }
