from fastapi import FastAPI
from routers.users import login, logout, signup

backend = FastAPI()

backend.include_router(login.router)
backend.include_router(logout.router)
backend.include_router(signup.router)

@backend.get("/api")
def test():
    return {"message": "Hello FastAPI"}