from typing import Any
from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
import os

router = APIRouter()

prefix_route = "/api/deck/create"

@router.post(prefix_route)
async def create_post(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "name" not in request_body or request_body["name"] is None or type(request_body["name"]) is not str:
		return JSONResponse({"status": 500, "message": "Missing new deck name"}, status_code=500)
	
	deck_name = request_body["name"]
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		new_deck = col.decks.new_deck()
		new_deck['name'] = deck_name
		col.decks.add_deck(new_deck)
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp