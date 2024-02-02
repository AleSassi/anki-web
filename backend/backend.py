from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.users import login, logout, signup
from routers.collection import collection
from routers.deck import overview, stats, options, create, study, custom_study
from routers.deck import cards as deck_cards
from routers.collection.models import models, fields
from routers.cards import cards, import_file

backend = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

backend.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)

backend.include_router(login.router)
backend.include_router(logout.router)
backend.include_router(signup.router)
backend.include_router(collection.router)
backend.include_router(overview.router)
backend.include_router(stats.router)
backend.include_router(options.router)
backend.include_router(create.router)
backend.include_router(study.router)
backend.include_router(custom_study.router)
backend.include_router(deck_cards.router)
backend.include_router(models.router)
backend.include_router(fields.router)
backend.include_router(import_file.router)
backend.include_router(cards.router)

@backend.get("/api")
def test():
    return {"message": "Hello FastAPI"}