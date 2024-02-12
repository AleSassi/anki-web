from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ...users.auth import Auth
from ..helpers import get_collection
import os

router = APIRouter()

prefix_route = "/api/collection/models"

@router.get(prefix_route)
async def models_get(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = request.query_params
	all_models = True
	model_id = 0
	if request_body.get("model_id") is not None:
		all_models = False
		model_id: int = int(request_body.get("model_id"))
	
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}
	
	if col is not None:
		if all_models:
			resp_data = {
				"models": [{
					"id": model.id,
					"name": model.name
				} for model in col.models.all_names_and_ids()]
			}
		else:
			resp_data = {
				"model": col.models.get(model_id)
			}
		col.close()
	
	resp = JSONResponse(resp_data)
	return resp

@router.post(prefix_route)
async def models_post(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - proceed with file upload

	return JSONResponse({"status": 500, "message": "Not implemented (yet)"}, status_code=500)
	
	request_body = await request.json()
	if "model_name" not in request_body or request_body["model_name"] is None or type(request_body["model_name"]) is not str:
		return JSONResponse({"status": 500, "message": "Missing model name"}, status_code=500)
	if "src_model_id" not in request_body or request_body["src_model_id"] is None or type(request_body["src_model_id"]) is not int:
		return JSONResponse({"status": 500, "message": "Missing model ID to copy"}, status_code=500)
	
	col = get_collection(token_data)
	model_name = request_body["model_name"]
	src_model_id = request_body["src_model_id"]
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		src_model = col.models.get(int(src_model_id))
		if src_model is None:
			return JSONResponse({"status": 500, "message": "No model with given ID found"}, status_code=500)
		copied_model = col.models.copy(src_model)
		copied_model["name"] = model_name
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp

@router.put(prefix_route)
async def models_put(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - proceed with file upload
	
	request_body = await request.json()
	if "model_name" not in request_body or request_body["model_name"] is None or type(request_body["model_name"]) is not str:
		return JSONResponse({"status": 500, "message": "Missing model name"}, status_code=500)
	if "src_model_id" not in request_body or request_body["src_model_id"] is None or type(request_body["src_model_id"]) is not int:
		return JSONResponse({"status": 500, "message": "Missing model ID to copy"}, status_code=500)
	
	col = get_collection(token_data)
	model_name = request_body["model_name"]
	src_model_id = request_body["src_model_id"]
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		src_model = col.models.get(int(src_model_id))
		if src_model is None:
			return JSONResponse({"status": 500, "message": "No model with given ID found"}, status_code=500)
		copied_model = col.models.copy(src_model)
		copied_model["name"] = model_name
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp