from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
from .stats_builder import RESTCollectionStats, PERIOD_LIFE, PERIOD_MONTH, PERIOD_YEAR
import os

router = APIRouter()

prefix_route = "/api/deck/stats"

@router.get(prefix_route)
async def stats_get(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "deck_id" not in request_body or request_body["deck_id"] is None:
		return JSONResponse({"status": 500, "message": "Missing deck ID"}, status_code=500)
	
	stats_period = PERIOD_MONTH
	did = request_body["deck_id"]
	if "stats_period" in request_body and request_body["stats_period"] is not None:
		stats_period_str = str(request_body["stats_period"])
		if stats_period_str == "lifetime":
			stats_period = PERIOD_LIFE
		elif stats_period_str == "year":
			stats_period = PERIOD_YEAR
		else:
			stats_period = PERIOD_MONTH

	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		if did:
			col.decks.select(int(did))
		stats = RESTCollectionStats(col).report_data(stats_period)
		col.close()
		
		resp_data = {
			"status": 200,
			"data": stats
		}
	
	resp =  JSONResponse(resp_data)
	return resp