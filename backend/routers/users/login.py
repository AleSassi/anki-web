from fastapi import Depends
from .auth import Auth
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request

router = APIRouter()

prefix_route = "/api/login"

@router.post(prefix_route)
async def login_post(request: Request):
    auth = Auth()
    request_json = await request.json()
    if "username" not in request_json or not request_json['username']:
        return JSONResponse({"status": 500, "Message": "Username is missing"})
    elif "password" not in request_json or not request_json['password']:
        return JSONResponse({"status": 500, "Message": "Password is missing"})
    
    username = request_json['username']
    password = request_json['password']
    token = auth.login_for_access_token(username=username, password=password)
    resp =  JSONResponse({"status": 200, "message": "Login successful"})
    resp.set_cookie(key="auth", value=token)
    return resp
