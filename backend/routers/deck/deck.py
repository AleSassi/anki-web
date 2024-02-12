from typing import Any
from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
import os

router = APIRouter()

prefix_route = "/api/deck"

@router.delete(prefix_route)
async def delete_deck(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "deck_id" not in request_body or request_body["deck_id"] is None or type(request_body["deck_id"]) is not int:
		raise HTTPException(status_code=500, detail="Missing deck ID")
	
	deck_id = request_body["deck_id"]
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		col.decks.remove([deck_id])
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp