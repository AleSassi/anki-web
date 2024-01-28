from typing import Any
from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
from anki.scheduler_pb2 import CustomStudyRequest
import os

router = APIRouter()

prefix_route = "/api/deck/custom-study"

"""
message CustomStudyRequest {
  message Cram {
    enum CramKind {
      // due cards in due order
      CRAM_KIND_DUE = 0;
      // new cards in added order
      CRAM_KIND_NEW = 1;
      // review cards in random order
      CRAM_KIND_REVIEW = 2;
      // all cards in random order; no rescheduling
      CRAM_KIND_ALL = 3;
    }
    CramKind kind = 1;
    // the maximum number of cards
    uint32 card_limit = 2;
    // cards must match one of these, if unempty
    repeated string tags_to_include = 3;
    // cards must not match any of these
    repeated string tags_to_exclude = 4;
  }
  int64 deck_id = 1;
  oneof value {
    // increase new limit by x
    int32 new_limit_delta = 2;
    // increase review limit by x
    int32 review_limit_delta = 3;
    // repeat cards forgotten in the last x days
    uint32 forgot_days = 4;
    // review cards due in the next x days
    uint32 review_ahead_days = 5;
    // preview new cards added in the last x days
    uint32 preview_days = 6;
    Cram cram = 7;
  }
}
"""

@router.post(prefix_route)
async def custom_study_post(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "request" not in request_body or request_body["request"] is None or type(request_body["request"]) is not dict:
		return JSONResponse({"status": 500, "message": "Missing custom study request"}, status_code=500)
	
	custom_study_req: dict[str, Any] = request_body["request"]

	keys = ["deck_id", ["new_limit_delta", "review_limit_delta", "forgot_days", "review_ahead_days", "preview_days", "cram"]]
	cram_keys = ["kind", "card_limit", "tags_to_include", "tags_to_exclude"]
	valid = True
	for key in keys:
		if key is str:
			valid = valid and key in custom_study_req
		else:
			valid2 = False
			for key2 in key:
				valid2 = key2 in custom_study_req
				if valid2:
					break
			valid = valid and valid2
	if valid and "cram" in custom_study_req:
		for key in cram_keys:
			valid = valid and key in custom_study_req["cram"]
	if not valid:
		return JSONResponse({"status": 500, "message": "Invalid custom study request"}, status_code=500)

	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		study_req = {
			"deck_id": custom_study_req["deck_id"]
		}
		for k in keys[1]:
			if k in custom_study_req:
				study_req[k] = custom_study_req[k]
				break
		
		col.sched.custom_study(study_req)
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp