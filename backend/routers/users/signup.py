from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from .auth import Auth
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

prefix_route = "/api/signup"

@router.post(prefix_route)
async def signup_post(request: Request):
    auth = Auth()

    request_json = await request.json()
    if "username" not in request_json or not request_json['username']:
        raise HTTPException(
            status_code=500,
            detail="Username is missing",
        )
    elif "password" not in request_json or not request_json['password']:
        raise HTTPException(
            status_code=500,
            detail="Password is missing",
        )

    username = request_json['username']
    password = request_json['password']
    if len(username) == 0 or len(password) == 0:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
    if auth.get_user(username):
        raise HTTPException(
            status_code=500,
            detail="Username already exists",
        )
    elif len(password) < 8:
        raise HTTPException(
            status_code=500,
            detail="Password must be >= 8 chars long",
        )

    auth.add_user(username, password)
    return {"status": 200, "message": "Signup successful"}