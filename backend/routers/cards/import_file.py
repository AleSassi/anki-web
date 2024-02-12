import codecs
import shutil
from typing import Any, Annotated
from fastapi import Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
import os, csv, json

router = APIRouter()

prefix_route = "/api/cards/import-file"

@router.put(prefix_route)
async def card_file_put(request: Request, file: Annotated[UploadFile, File()], request_body_str: Annotated[str, Form()]):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks
	
	request_body: dict = json.loads(request_body_str)
	if "deck_id" not in request_body or request_body["deck_id"] is None or type(request_body["deck_id"]) is not int:
		raise HTTPException(status_code=500, detail="Missing parent deck ID")
	if "model_id" not in request_body or request_body["model_id"] is None or type(request_body["model_id"]) is not int:
		raise HTTPException(status_code=500, detail="Missing model ID for cards (the same for all cards)")
	
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
			raise HTTPException(status_code=500, detail="No model with given ID was found")
		model_fields: list[dict] = model["flds"]
		model_fields.sort(key=lambda field: field["ord"])
		
		try:
			csvFileReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
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
		except Exception as e:
			print(e.with_traceback(None))
			raise HTTPException(status_code=500, detail="There was an error uploading the file")
		finally:
			file.file.close()
		
		col.save()
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp