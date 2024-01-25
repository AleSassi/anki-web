from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
import os

router = APIRouter()

prefix_route = "/api/deck/overview"

@router.get(prefix_route)
async def overview_get(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "deck_id" not in request_body or request_body["deck_id"] is None:
		return JSONResponse({"status": 500, "message": "Missing deck ID"}, status_code=500)
	
	did = request_body["deck_id"]
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}
	if col is not None:
		decks = col.decks
		if did:
			col.decks.select(int(did))
		deck = decks.current()
		sched = col.sched
		sched.reset()
		newCount, lrnCount, revCount = sched.counts()
		finished = not sum([newCount, lrnCount, revCount])
		col.close()
		
		resp_data = {
			"status": 200,
			"data": {
				"deck": deck,
				"new_count": newCount,
				"lrn_count": lrnCount,
				"rev_count": revCount,
				"finished": finished
			}}
	
	resp =  JSONResponse(resp_data)
	return resp