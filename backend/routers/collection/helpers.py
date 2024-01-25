import sqlite3
from ..users.auth import TokenData
from ..users.session import SessionStorage
from anki.storage import Collection

def get_collection_path(username: str) -> str:
    return "/app/data/" + username + '/collection.anki2'

def get_collection(token: TokenData) -> Collection:
    col = SessionStorage.get(token.session_id, "_collection")
    if col is None:
        collection_path = get_collection_path(token.username)
        col = Collection(collection_path)
        SessionStorage.set(token.session_id, "_collection", col)
    return col