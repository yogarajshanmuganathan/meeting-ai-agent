from fastapi import APIRouter
import requests
from app.services import token_store

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/events")
def get_events():

    if not token_store.ACCESS_TOKEN:
        return {"error": "Not authenticated. Please login first."}

    # Decode token to see scopes
    import json
    import base64
    try:
        parts = token_store.ACCESS_TOKEN.split('.')
        decoded = base64.urlsafe_b64decode(parts[1] + '==')
        payload = json.loads(decoded)
        print(f"TOKEN SCOPES: {payload.get('scp', 'NO SCOPES')}")
    except:
        pass

    headers = {
        "Authorization": f"Bearer {token_store.ACCESS_TOKEN}"
    }

    try:
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me/events",
            headers=headers
        )
        
        # Check status code first
        if response.status_code != 200:
            return {
                "error": f"Microsoft API returned {response.status_code}",
                "details": response.text
            }
        
        return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch events: {str(e)}"}