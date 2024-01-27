from typing import Any
from fastapi import Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from ..users.auth import Auth
from ..collection.helpers import get_collection, get_collection_path
from anki.decks import DeckConfigId
import os

router = APIRouter()

prefix_route = "/api/deck/options"

"""
An example settings dict:
{
	"id": 1, 						# The ID of this model
	"mod": 1704718770,				# ??????
	"name": "Default",				# Model name
	"usn": -1,						#
	"maxTaken": 60,					# Timer - Max answer seconds
	"autoplay": False,				# Auto-play audio
	"timer": 0,						# Show answer timer?
	"replayq": True,				#
	"new": {						# 
		"bury": False,
		"delays": [					# Learning steps
			1.0,
			10.0
		],
		"initialFactor": 2500,
		"ints": [					# Intervals
			1,						#	Graduating interval
			4,						#	Easy interval
			0
		],
		"order": 1,					# Insertion order (1 = sequential, other???)
		"perDay": 15				# New cards per day
	},
	"rev": {
		"bury": False,
		"ease4": 1.3,				# Advanced - Easy bonus
		"ivlFct": 1.0,				# Advanced - Interval modifier
		"maxIvl": 36500,			# Advanced - Max interval
		"perDay": 200,				# Max reviews per day
		"hardFactor": 1.2			# Advanced - Hard interval
	},
	"lapse": {						# Lapses
		"delays": [					#	Relearning steps
			10.0
		],
		"leechAction": 1,			#	Leech action (1 = Tag only, other???)
		"leechFails": 8,			#	Leech threshold
		"minInt": 1,				#	Minimum interval
		"mult": 0.0
	},
	"dyn": False,
	"newMix": 0,
	"newPerDayMinimum": 0,
	"interdayLearningMix": 0,
	"reviewOrder": 0,
	"newSortOrder": 0,
	"newGatherPriority": 0,
	"buryInterdayLearning": False
}

From AnkiDroid documentation (outdated)
{
"deck config id (creation time in epoch milliseconds for most option groups, '1' for the default option group)" :
  {
		autoplay :      "whether the audio associated to a question should be played when the question is shown"
		dyn :           "Whether this deck is dynamic. Not present by default in decks.py"
		id :            "deck ID (automatically generated long). Not present by default in decks.py"
		lapse : {       "The configuration for lapse cards."
			delays :        "The list of successive delay between the learning steps of the new cards, as explained in the manual."
			leechAction :   "What to do to leech cards. 0 for suspend, 1 for mark. Numbers according to the order in which the choices appear in aqt/dconf.ui"
			leechFails :    "the number of lapses authorized before doing leechAction."
			minInt:         "a lower limit to the new interval after a leech"
			mult :          "percent by which to multiply the current interval when a card goes has lapsed"
		}
		maxTaken :      "The number of seconds after which to stop the timer"
		mod :           "Last modification time"
		name :          "The name of the configuration"
		new : {         "The configuration for new cards."
			bury :          "Whether to bury cards related to new cards answered"
			delays :        "The list of successive delay between the learning steps of the new cards, as explained in the manual."
			initialFactor : "The initial ease factor"
			ints :          "The list of delays according to the button pressed while leaving the learning mode. Good, easy and unused. In the GUI, the first two elements corresponds to Graduating Interval and Easy interval"
			order :         "In which order new cards must be shown. NEW_CARDS_RANDOM = 0 and NEW_CARDS_DUE = 1."
			perDay :        "Maximal number of new cards shown per day."
			separate :      "Seems to be unused in the code."
		}
		replayq :       "whether the audio associated to a question should be played when the answer is shown"
		rev : {         "The configuration for review cards."
			bury :          "Whether to bury cards related to new cards answered"
			ease4 :         "the number to add to the easyness when the easy button is pressed"
			fuzz :          "The new interval is multiplied by a random number between -fuzz and fuzz"
			ivlFct :        "multiplication factor applied to the intervals Anki generates"
			maxIvl :        "the maximal interval for review"
			minSpace :      "not currently used according to decks.py code's comment"
			perDay :        "Numbers of cards to review per day"
		}
		timer :         "whether timer should be shown (1) or not (0)"
		usn :           "See usn in cards table for details."
  }
}
"""

@router.get(prefix_route)
async def options_get(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "options_id" not in request_body or request_body["options_id"] is None:
		return JSONResponse({"status": 500, "message": "Missing options ID"}, status_code=500)
	
	optid = request_body["options_id"]
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		deck_conf = col.decks.get_config(DeckConfigId(optid))
		
		resp_data = {
			"status": 200,
			"data": {
				"config": {
					"id": deck_conf['id'],
					"last_modification_timestamp": deck_conf['mod'],
					"name": deck_conf['name'],
					"is_default": deck_conf['id'] == 1,
					"answer_timer_stop_after_secs": deck_conf['maxTaken'],
					"autoplay_audio_on_question": deck_conf['autoplay'],
					"should_show_timer": False if deck_conf['timer'] == 0 else True,
					"autoplay_audio_on_answer": deck_conf['replayq'],
					"new_cards_config": {
						"should_bury": deck_conf['new']['bury'],
						"learning_steps_delays": deck_conf['new']['delays'],
						"initial_ease_factor": deck_conf['new']['initialFactor'],
						"intervals": {
							"graduating": deck_conf['new']['ints'][0],
							"easy": deck_conf['new']['ints'][1],
						},
						"new_cards_order": "SEQUENTIAL" if deck_conf['new']['order'] == 1 else "RANDOM",
						"max_per_day": deck_conf['new']['perDay']
					},
					"review_cards_config": {
						"bury": deck_conf['rev']['bury'],
						"easy_bonus": deck_conf['rev']['ease4'],
						"interval_mult_factor": deck_conf['rev']['ivlFct'],
						"max_review_interval": deck_conf['rev']['maxIvl'],
						"max_per_day": deck_conf['rev']['perDay'],
						"hard_interval_factor": deck_conf['rev']['hardFactor']
					},
					"lapse_cards": {
						"learning_steps_delays": deck_conf['lapse']['delays'],
						"on_leech_action": "SUSPEND" if deck_conf['lapse']['leechAction'] == 0 else "MARK",
						"lapses_to_leech": deck_conf['lapse']['leechFails'],
						"min_new_interval_after_leech": deck_conf['lapse']['minInt'],
						"perc_multiplied": deck_conf['lapse']['mult']
					},
					"deck_is_dynamic": deck_conf['dyn'],
					"newMix": deck_conf['newMix'],
					"newPerDayMinimum": deck_conf['newPerDayMinimum'],
					"interdayLearningMix": deck_conf['interdayLearningMix'],
					"reviewOrder": deck_conf['reviewOrder'],
					"newSortOrder": deck_conf['newSortOrder'],
					"newGatherPriority": deck_conf['newGatherPriority'],
					"buryInterdayLearning": deck_conf['buryInterdayLearning']
				}
			}
		}
	
	resp =  JSONResponse(resp_data)
	return resp

@router.post(prefix_route)
async def options_post(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "options_id" not in request_body or request_body["options_id"] is None:
		return JSONResponse({"status": 500, "message": "Missing options ID"}, status_code=500)
	if "config" not in request_body or request_body["config"] is None:
		return JSONResponse({"status": 500, "message": "Missing configuration updates"}, status_code=500)
	
	optid = request_body["options_id"]
	new_conf: dict[str, Any] = request_body["config"]
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		deck_conf = col.decks.get_config(DeckConfigId(optid))
		
		new_ans_timer = new_conf.get('answer_timer_stop_after_secs')
		new_autoplay_on_question = new_conf.get('autoplay_audio_on_question')
		new_show_timer = new_conf.get('should_show_timer')
		new_autoplay_audio_answer = new_conf.get('autoplay_audio_on_answer')
		if new_ans_timer is not None and type(new_ans_timer) is int and new_ans_timer > 0:
			deck_conf['maxTaken'] = new_ans_timer
		if new_autoplay_on_question is not None and type(new_autoplay_on_question) is bool:
			deck_conf['autoplay'] = new_autoplay_on_question
		if new_show_timer is not None and type(new_show_timer) is bool:
			deck_conf['should_show_timer'] = 1 if new_show_timer else 0
		if new_autoplay_audio_answer is not None and type(new_autoplay_audio_answer) is bool:
			deck_conf['replayq'] = new_autoplay_audio_answer
		
		new_new_cards_conf = new_conf.get('new_cards_config')
		if new_new_cards_conf is not None and type(new_new_cards_conf) is dict:
			should_bury = new_new_cards_conf.get('should_bury')
			learning_steps_delays = new_new_cards_conf.get('learning_steps_delays')
			initial_ease_factor = new_new_cards_conf.get('initial_ease_factor')
			new_cards_order = new_new_cards_conf.get('new_cards_order')
			max_per_day = new_new_cards_conf.get('max_per_day')
			intervals = new_new_cards_conf.get('intervals')

			if should_bury is not None and type(should_bury) is bool:
				deck_conf['new']['bury'] = should_bury
			if learning_steps_delays is not None and type(learning_steps_delays) is list:
				deck_conf['new']['delays'] = learning_steps_delays
			if initial_ease_factor is not None and type(initial_ease_factor) is int:
				deck_conf['new']['initialFactor'] = initial_ease_factor
			if new_cards_order is not None and type(new_cards_order) is str:
				if new_cards_order == "SEQUENTIAL":
					deck_conf['new']['order'] = 1
				elif new_cards_order == "RANDOM":
					deck_conf['new']['order'] = 0
			if max_per_day is not None and type(max_per_day) is int:
				deck_conf['new']['perDay'] = max_per_day
			if intervals is not None and type(intervals) is dict:
				new_grad = intervals.get("graduating")
				new_easy = intervals.get("easy")
				new_intervals = deck_conf['new']['ints']

				if new_grad is not None and type(new_grad) is int:
					new_intervals[0] = new_grad
				if new_easy is not None and type(new_easy) is int:
					new_intervals[1] = new_easy
				
				deck_conf['new']['ints'] = new_intervals
		
		new_rev_cards_conf = new_conf.get('review_cards_config')
		if new_rev_cards_conf is not None and type(new_rev_cards_conf) is dict:
			bury = new_rev_cards_conf.get('bury')
			easy_bonus = new_rev_cards_conf.get('easy_bonus')
			interval_mult_factor = new_rev_cards_conf.get('interval_mult_factor')
			max_review_interval = new_rev_cards_conf.get('max_review_interval')
			max_per_day = new_rev_cards_conf.get('max_per_day')
			hard_interval_factor = new_rev_cards_conf.get('hard_interval_factor')

			if bury is not None and type(bury) is bool:
				deck_conf['rev']['bury'] = bury
			if easy_bonus is not None and type(easy_bonus) is float:
				deck_conf['rev']['ease4'] = easy_bonus
			if interval_mult_factor is not None and type(interval_mult_factor) is float:
				deck_conf['rev']['ivlFct'] = interval_mult_factor
			if max_review_interval is not None and type(max_review_interval) is int:
				deck_conf['rev']['maxIvl'] = max_review_interval
			if max_per_day is not None and type(max_per_day) is int:
				deck_conf['rev']['perDay'] = max_per_day
			if hard_interval_factor is not None and type(hard_interval_factor) is float:
				deck_conf['rev']['hardFactor'] = hard_interval_factor
		
		new_lapse_cards_conf = new_conf.get('lapse_cards')
		if new_lapse_cards_conf is not None and type(new_lapse_cards_conf) is dict:
			learning_steps_delays = new_lapse_cards_conf.get('learning_steps_delays')
			on_leech_action = new_lapse_cards_conf.get('on_leech_action')
			lapses_to_leech = new_lapse_cards_conf.get('lapses_to_leech')
			min_new_interval_after_leech = new_lapse_cards_conf.get('min_new_interval_after_leech')
			perc_multiplied = new_lapse_cards_conf.get('perc_multiplied')

			if learning_steps_delays is not None and type(learning_steps_delays) is list[float]:
				deck_conf['lapse']['delays'] = learning_steps_delays
			if on_leech_action is not None and type(on_leech_action) is str:
				deck_conf['lapse']['leechAction'] = 0 if on_leech_action == "SUSPEND" else 1
			if lapses_to_leech is not None and type(lapses_to_leech) is int:
				deck_conf['lapse']['leechFails'] = lapses_to_leech
			if min_new_interval_after_leech is not None and type(min_new_interval_after_leech) is int:
				deck_conf['lapse']['minInt'] = min_new_interval_after_leech
			if perc_multiplied is not None and type(perc_multiplied) is float:
				deck_conf['lapse']['mult'] = perc_multiplied
		
		col.decks.update_config(deck_conf)
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp

@router.put(prefix_route)
async def options_put(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "new_preset_name" not in request_body or request_body["new_preset_name"] is None or type(request_body["new_preset_name"]) is not str:
		return JSONResponse({"status": 500, "message": "Missing preset name"}, status_code=500)
	
	new_preset_name = request_body["new_preset_name"]
	preset_id_to_clone = None # Default to option set creation
	if "preset_id_to_clone" in request_body and request_body["preset_id_to_clone"] is not None and type(request_body["preset_id_to_clone"]) is int:
		preset_id_to_clone = request_body["preset_id_to_clone"]
	
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		conf_to_clone = None
		if preset_id_to_clone is not None:
			conf_to_clone = col.decks.get_config(DeckConfigId(preset_id_to_clone))
		col.decks.add_config(new_preset_name, conf_to_clone)
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp

@router.delete(prefix_route)
async def options_delete(request: Request):
	auth = Auth()
	#Check authentication
	token_data = auth.check_login(request)
	#We are authenticated - return the list of decks

	request_body = await request.json()
	if "options_id" not in request_body or request_body["options_id"] is None or type(request_body["options_id"]) is not int:
		return JSONResponse({"status": 500, "message": "Missing options ID"}, status_code=500)
	
	optid = request_body["options_id"]
	col = get_collection(token_data)
	resp_data = {
		"status": 200,
		"data": {}
	}

	if col is not None:
		col.decks.remove_config(DeckConfigId(optid))
		col.close()
	
	resp =  JSONResponse(resp_data)
	return resp