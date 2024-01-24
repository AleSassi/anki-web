from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from .auth import Auth
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

prefix_route = "/signup"

@router.post(prefix_route)
async def signup_post(request: Request):
    auth = Auth()

    request_json = await request.json()
    if "username" not in request_json or not request_json['username']:
        return JSONResponse({"status": 500, "Message": "Username is missing"})
    elif "password" not in request_json or not request_json['password']:
        return JSONResponse({"status": 500, "Message": "Password is missing"})

    username = request_json['username']
    password = request_json['password']
    if auth.get_user(username):
        return {"status": 500, "message": "Username already exists"}
    elif len(password) < 8:
        return {"status": 500, "message": "Password must be >= 8 chars long"}

    auth.add_user(username, password)
    return {"status": 200, "message": "Signup successful"}