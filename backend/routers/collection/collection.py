from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ..users.auth import Auth
from helpers import get_collection, get_collection_path
import os

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

@router.put(prefix_route)
def collection_put(request: Request, file: UploadFile = File(...)):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - proceed with file upload
    
	is_sqlite = False
	coll_path = get_collection_path(token_data.username)
	try:
		with open(coll_path, 'wb') as f:
			while contents := file.file.read(1024 * 1024):
				f.write(contents)
			#Check that the file being written is an Anki collection
			is_sqlite = isSQLite3(coll_path)
	except Exception:
		return JSONResponse({"message": "There was an error uploading the file"}, status_code=500)
	finally:
		file.file.close()
	 
	if not is_sqlite:
		os.remove(coll_path)
		return JSONResponse({"message": "File is not an Anki collection database"}, status_code=500)
	
	return JSONResponse({"message": f"Successfully uploaded collection '{file.filename}'"})

def build_deck_list(decks: list) -> [dict]:
	deck_list = []
	for node in decks:
		name, did, due, lrn, new, children = node
		if did == 1:
			continue
		deck_list.append({'name': name, 'did': did, 'new': new, 'due': due, 'lrn': lrn, 'children': build_deck_list(children)})
	return deck_list

def isSQLite3(filename):
    from os.path import isfile, getsize
    if not isfile(filename):
        return False
    if getsize(filename)< 100: # SQLite database file header is 100 bytes
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)

    return header[:16] == 'SQLite format 3\x00'