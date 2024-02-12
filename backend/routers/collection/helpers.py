import sqlite3
from ..users.auth import TokenData
from ..users.session import SessionStorage
from anki.storage import Collection
import os

def get_collection_path(username: str) -> str:
    basedir = "/app/data/" + username
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    return basedir + '/collection.anki2'

def get_collection(token: TokenData) -> Collection | None:
    col = None#SessionStorage.get(token.session_id, "_collection")
    if col is None:
        collection_path = get_collection_path(token.username)
        if not os.path.exists(collection_path):
            return None
        col = Collection(collection_path)
        SessionStorage.set(token.session_id, "_collection", col)
    return col