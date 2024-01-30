from typing import Any
from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
import os, csv

router = APIRouter()

prefix_route = "/api/cards/import-file"

@router.put(prefix_route)
async def card_file_put(request: Request, file: UploadFile = File(...)):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body: dict = await request.json()
	if "deck_id" not in request_body or request_body["deck_id"] is None or type(request_body["deck_id"]) is not int:
		return JSONResponse({"status": 500, "message": "Missing parent deck ID"}, status_code=500)
	if "model_id" not in request_body or request_body["model_id"] is None or type(request_body["model_id"]) is not int:
		return JSONResponse({"status": 500, "message": "Missing model ID for cards (the same for all cards)"}, status_code=500)
	
	did = request_body['deck_id']
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
			return JSONResponse({"status": 500, "message": "No model with given ID was found"}, status_code=500)
		model_fields: list[dict] = model["flds"]
		model_fields.sort(key=lambda field: field["ord"])
		
		try:
			with open(file.file, newline='') as csvfile:
				csvFileReader = csv.DictReader(csvfile)
				for row in csvFileReader:
					note = col.new_note({"id": model["id"]})
					for field_dict in model_fields:
						field_data = row.get(field_dict["name"])
						note.fields[field_dict["ord"]] = field_data if field_data is not None else ''
					# Replace None with ''
					for i in range(0, len(note.fields)):
						if note.fields[i] is None:
							note.fields[i] = ''
					col.add_note(note, did)
		except Exception:
			return JSONResponse({"message": "There was an error uploading the file"}, status_code=500)
		finally:
			file.file.close()
		
		col.save()
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp