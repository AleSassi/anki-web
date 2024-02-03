from typing import Any
from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Request
from ..users.auth import Auth
from ..users.session import SessionStorage
from ..collection.helpers import get_collection, get_collection_path
import os, html, re

router = APIRouter()

prefix_route = "/api/deck/study"

def all_sounds(text):
    _soundReg = r"\[sound:(.*?)\]"
    match = re.findall(_soundReg, text)
    sound_list = list(map(html.unescape, match))
    return sound_list

@router.get(prefix_route)
async def study_get(request: Request):
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
		"status": 200,
		"data": {}
	}

	if col is not None:
		if deck_id:
			col.decks.select(int(deck_id))
		col.reset()
		card = col.sched.getCard()
		if card is None:
			col.close()
			return {
				"finished": True
			}
		else:
			question = card.question()
			answer = card.answer()
			currDid = card.did
			if currDid:
				dueTree = col.sched.deckDueTree()
				for node in dueTree:
					name, did, due, lrn, new, children = node
					if did == 1:
						continue
					if did == currDid:
						newCount = new
						lrnCount = lrn
						revCount = due
						break
					found_subdeck = False
					for sub_node in children:
						sub_name, sub_did, sub_due, sub_lrn, sub_new, sub_children = sub_node
						if sub_did == currDid:
							newCount = sub_new
							lrnCount = sub_lrn
							revCount = sub_due
							found_subdeck = True
							break
					if found_subdeck:
						break
			
			cardType = card.queue
			newClass = ""
			lrnClass = ""
			dueClass = ""
			if cardType == 0:
				newClass = "text-decoration-underline"
			elif cardType == 1:
				lrnClass = "text-decoration-underline"
			else:
				dueClass = "text-decoration-underline"
			
			question_sound_list = all_sounds(question)
			answer_sound_list = all_sounds(answer)
			
			question = re.sub(r"\[sound:[^]]+\]", "", question)
			answer = re.sub(r"\[sound:[^]]+\]", "", answer)

			reMedia = re.compile("(?i)(<img[^>]+src=[\"']?)([^\"'>]+[\"']?[^>]*>)")
			media_url_prefix = "/api/deck/media?filename="
			question = reMedia.sub(" \\1" + media_url_prefix + "\\2", question)
			answer = reMedia.sub(" \\1" + media_url_prefix + "\\2", answer)

			cnt = col.sched.answerButtons(card)
			if cnt == 2:
				btn_list = [(1, 'Again', col.sched.nextIvlStr(card, 1)), (2, 'Good', col.sched.nextIvlStr(card, 2))]
			elif cnt == 3:
				btn_list = [(1, 'Again', col.sched.nextIvlStr(card, 1)), (2, 'Good', col.sched.nextIvlStr(card, 2)), (3, 'Easy', col.sched.nextIvlStr(card, 3))]
			else:
				btn_list = [(1, 'Again', col.sched.nextIvlStr(card, 1)), (2, 'Hard', col.sched.nextIvlStr(card, 2)), (3, 'Good', col.sched.nextIvlStr(card, 3)), (4, 'Easy', col.sched.nextIvlStr(card, 4))]
			col.close()
			
			SessionStorage.set(token_data.session_id, "_active_card", card)

			btn_list_json = []
			for btn in btn_list:
				btn_list_json.append({
					"id": btn[0],
					"title": btn[1],
					"interval": btn[2]
				})
			resp_data = {
				"finished": False,
				"card_data": {
					"question": {
						"html_text": question,
						"sounds": question_sound_list
					},
					"answer": {
						"html_text": answer,
						"sounds": answer_sound_list
					},
					"buttons": btn_list_json,
					"card_type": cardType,
					"counts": {
						"unseen": newCount,
						"learning": lrnCount,
						"revising": revCount
					}
				}
			}
	
	resp =  JSONResponse(resp_data)
	return resp

@router.post(prefix_route)
async def study_post(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "deck_id" not in request_body or request_body["deck_id"] is None or type(request_body["deck_id"]) is not int:
		raise HTTPException(status_code=500, detail="Missing deck ID")
	if "answer_id" not in request_body or request_body["answer_id"] is None or type(request_body["answer_id"]) is not int:
		raise HTTPException(status_code=500, detail="Missing answer ID")
	
	deck_id = request_body["deck_id"]
	answer_id = request_body["answer_id"]
	col = get_collection(token_data)
	resp_data = {
		"answered": False
	}

	if col is not None:
		if deck_id:
			col.decks.select(int(deck_id))
		col.reset()
		activeCard = SessionStorage.get(token_data.session_id, "_active_card")
		if activeCard is None:
			raise HTTPException(status_code=500, detail="No active card")
		else:
			activeCard.col = col
			activeCard.note().col = col
			sched = col.sched
			sched.answerCard(activeCard, int(answer_id))
			col.close()
			SessionStorage.set(token_data.session_id, "_answer_card", None)
			resp_data = {
				"answered": True
			}
	
	return JSONResponse(resp_data)