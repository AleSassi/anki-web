from fastapi import FastAPI
from routers.users import login, logout, signup
from routers.collection import collection
from routers.deck import overview, stats, options, create, study, custom_study
from routers.deck import cards as deck_cards
from routers.collection.models import models, fields
from routers.cards import cards, import_file

backend = FastAPI()

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