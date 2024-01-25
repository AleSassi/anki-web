from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ..users.auth import Auth
from helpers import get_collection

router = APIRouter()

prefix_route = "/api/collection"

@router.get(prefix_route)
def collection_get(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks
    
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}
	if col is not None:
		dueTree = col.sched.deckDueTree()
		deck_list = build_deck_list(dueTree)

		cards, studiedTime = col.db.first("select count(), sum(time)/1000 from revlog where id > ?", (col.sched.dayCutoff - 86400) * 1000)
		col.close()

		if cards is None:
			cards = 0
		if studiedTime is None:
			studiedTime = 0
		
		resp_data = {
			"status": 200,
			"data": {
				"decks": deck_list,
				"studiedCards": cards,
				"studiedTime": studiedTime
			}}
	
	resp =  JSONResponse(resp_data)
	return resp

def build_deck_list(decks: list) -> [dict]:
	deck_list = []
	for node in decks:
		name, did, due, lrn, new, children = node
		if did == 1:
			continue
		deck_list.append({'name': name, 'did': did, 'new': new, 'due': due, 'lrn': lrn, 'children': build_deck_list(children)})
	return deck_list