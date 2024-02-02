from fastapi import Depends
from .auth import Auth
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Request, Response
import datetime

router = APIRouter()

prefix_route = "/api/login"

@router.post(prefix_route)
async def login_post(request: Request):
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
    token = auth.login_for_access_token(username=username, password=password)
    resp =  JSONResponse({"status": 200, "message": "Login successful"})
    resp.set_cookie(key="auth", value=token, httponly=True, max_age=1800, expires=1800, samesite='strict', secure=False,)
    return resp
