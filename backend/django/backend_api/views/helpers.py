from anki.storage import Collection
from pathlib import Path
from ..models import User


def get_collection_path(username):
    return "/anki-data/" + username + "/collection.anki2"


def get_collection(session):
    col = session.get("collection")
    if col is not None:
        return col

    uid = session.get("_auth_user_id")
    user = User.objects.get(id=uid)
    username = user.username
    collection_path = get_collection_path(username)
    collection_path_object = Path(collection_path)
    if collection_path_object.exists():
        col = Collection(collection_path)
        session["collection"] = col
        return col

    return None
