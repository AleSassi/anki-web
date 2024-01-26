from fastapi import FastAPI
from routers.users import login, logout, signup
from routers.collection import collection
from routers.deck import overview, stats

backend = FastAPI()

backend.include_router(login.router)
backend.include_router(logout.router)
backend.include_router(signup.router)
backend.include_router(collection.router)
backend.include_router(overview.router)
backend.include_router(stats.router)

@backend.get("/api")
def test():
    return {"message": "Hello FastAPI"}