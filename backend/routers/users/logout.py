from fastapi import Depends, HTTPException, Response
from .auth import Auth
from fastapi import APIRouter

router = APIRouter()

prefix_route = "/api/logout"

@router.post(prefix_route)
def logout_post(response: Response):
    response.delete_cookie("auth")
    return {"status": 200, "message": "Logout successful"}