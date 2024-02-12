from typing import Any
from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
import os

router = APIRouter()

prefix_route = "/api/cards"

@router.post(prefix_route)
async def card_post(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body: dict = await request.json()
	if "card_id" not in request_body or request_body["card_id"] is None or type(request_body["card_id"]) is not int:
		raise HTTPException(status_code=500, detail="Missing card ID")
	if "fields" not in request_body or request_body["fields"] is None or type(request_body["fields"]) is not list:
		raise HTTPException(status_code=500, detail="Missing new data for card fields")
	
	cid = request_body['card_id']
	fields: list[dict] = request_body["fields"]
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		card = col.get_card(int(cid))
		note = card.note()
		note_fields = note.items()
		for field in note_fields:
			newVal: str = None
			for req_fields in fields:
				if req_fields.get("name") == field[0]:
					newVal = req_fields.get("value")
					break
			
			if newVal is not None and type(newVal) is type(note[field[0]]):
				note[field[0]] = newVal
		col.update_note(note)
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp

@router.put(prefix_route)
async def card_put(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body: dict = await request.json()
	if "deck_id" not in request_body or request_body["deck_id"] is None or type(request_body["deck_id"]) is not int:
		raise HTTPException(status_code=500, detail="Missing parent deck ID")
	if "model_id" not in request_body or request_body["model_id"] is None or type(request_body["model_id"]) is not int:
		raise HTTPException(status_code=500, detail="Missing model ID for card")
	if "fields" not in request_body or request_body["fields"] is None or type(request_body["fields"]) is not list:
		raise HTTPException(status_code=500, detail="Missing new data for card fields")
	
	did = request_body['deck_id']
	fields: list[dict] = request_body["fields"]
	model_id: int = request_body["model_id"]
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		col.decks.select(int(did))
		model = col.models.get(model_id)
		if model is None:
			raise HTTPException(status_code=500, detail="No model with given ID was found")
		model_fields: list[dict] = model["flds"]
		model_fields.sort(key=lambda field: field["ord"])
		note = col.new_note({"id": model["id"]})
		for field_dict in model_fields:
			# Find the field in the input data
			input_field: dict | None = None
			for in_field in fields:
				if field_dict["name"] == in_field["name"]:
					input_field = in_field
					break
			if input_field is not None:
				note.fields[field_dict["ord"]] = input_field["value"]
		# Replace None with ''
		for i in range(0, len(note.fields)):
			if note.fields[i] is None:
				note.fields[i] = ''
		col.add_note(note, did)
		col.save()
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp

@router.delete(prefix_route)
async def card_delete(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body: dict = await request.json()
	if "card_ids" not in request_body or request_body["card_ids"] is None or type(request_body["card_ids"]) is not list:
		raise HTTPException(status_code=500, detail="Missing card ID")
	
	cid: list[int] = request_body['card_ids']
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		col.remove_notes_by_card(cid)
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp