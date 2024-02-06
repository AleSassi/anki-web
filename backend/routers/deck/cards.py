from typing import Any
from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
import os

router = APIRouter()

prefix_route = "/api/deck/cards"

@router.get(prefix_route)
async def deck_cards_get(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = request.query_params
	if request_body.get("deck_id") is None:
		raise HTTPException(status_code=500, detail="Missing deck ID")
	
	deck_id = int(request_body.get("deck_id"))
	col = get_collection(token_data)
	resp_data = {
		"cards": []
	}

	if col is not None:
		if deck_id:
			col.decks.select(deck_id)
		cards = col.decks.cids(deck_id)
		card_list = []
		for cardId in cards:
			card = col.get_card(cardId)
			note = card.note()
			cardTypes = ["New", "Study", "Learned", "Learned"]
			#card_list.append((note.items()[0][1], "Reverse" if card.ord == 1 else "Forward", cardTypes[card.type], cardId))
			card_dict_copy = dict(card.__dict__)
			del card_dict_copy["_note"]
			del card_dict_copy["_render_output"]
			del card_dict_copy["col"]
			del card_dict_copy["timer_started"]
			card_dict_copy["note"] = {
				"id": note.id,
				"guid": note.guid,
				"model_id": note.mid,
				"last_modified": note.mod,
				"usn": note.usn,
				"tags": note.tags,
				"fields": [{
					"name": f[0],
					"value": f[1]
				} for f in note.items()],
			}
			card_dict_copy["ord"] = "Reverse" if card.ord == 1 else "Forward"
			card_dict_copy["type"] = cardTypes[card.type]
			card_list.append(card_dict_copy)
		#No sorting - can be done by the client
		col.close()
		resp_data["cards"] = card_list
	
	resp =  JSONResponse(resp_data)
	return resp