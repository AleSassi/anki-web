from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from routers.users import login, logout, signup
from routers.collection import collection
from routers.deck import overview, stats, options, create, study, custom_study, deck
from routers.deck import cards as deck_cards
from routers.collection.models import models, fields
from routers.cards import cards, import_file
from dotenv import load_dotenv
import os, json

load_dotenv()

backend = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
env_origins = json.loads(os.getenv('FRONTEND_URLS'))
for env_origin in env_origins:
    origins.append(env_origin)

@backend.exception_handler(500)
async def custom_http_exception_handler(request, exc):
    detail = ""
    if type(exc) is HTTPException:
        httpexc: HTTPException = exc
        detail = httpexc.detail
    else:
        detail = "Internal server error"
    
    response = JSONResponse(content={
        "detail": detail
    }, status_code=500)

    # Since the CORSMiddleware is not executed when an unhandled server exception
    # occurs, we need to manually set the CORS headers ourselves if we want the FE
    # to receive a proper JSON 500, opposed to a CORS error.
    # Setting CORS headers on server errors is a bit of a philosophical topic of
    # discussion in many frameworks, and it is currently not handled in FastAPI. 
    # See dotnet core for a recent discussion, where ultimately it was
    # decided to return CORS headers on server failures:
    # https://github.com/dotnet/aspnetcore/issues/2378
    origin = request.headers.get('origin')

    if origin:
        # Have the middleware do the heavy lifting for us to parse
        # all the config, then update our response headers
        cors = CORSMiddleware(
                app=backend,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"])

        # Logic directly from Starlette's CORSMiddleware:
        # https://github.com/encode/starlette/blob/master/starlette/middleware/cors.py#L152

        response.headers.update(cors.simple_headers)
        has_cookie = "cookie" in request.headers

        # If request includes any cookie headers, then we must respond
        # with the specific origin instead of '*'.
        if cors.allow_all_origins and has_cookie:
            response.headers["Access-Control-Allow-Origin"] = origin

        # If we only allow specific origins, then we have to mirror back
        # the Origin header in the response.
        elif not cors.allow_all_origins and cors.is_allowed_origin(origin=origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers.add_vary_header("Origin")

    return response

backend.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
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
backend.include_router(deck.router)

@backend.get("/api")
def test():
    return {"message": "Hello FastAPI"}