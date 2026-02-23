from fastapi import APIRouter, Request
from app.services.auth_service import (
    get_auth_url,
    exchange_code_for_token,
    get_user_profile
)
from app.services import token_store

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/login")
def login():
    return {"auth_url": get_auth_url()}


@router.get("/callback")
def callback(request: Request):

    code = request.query_params.get("code")

    if not code:
        return {"error": "No code received"}

    token_response = exchange_code_for_token(code)

    if "access_token" not in token_response:
        return {"error": token_response}

    token_store.ACCESS_TOKEN = token_response["access_token"]

    profile = get_user_profile(token_store.ACCESS_TOKEN)

    return {
        "message": "Login successful",
        "user_profile": profile
    }