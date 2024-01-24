from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
from helpers import *
from rest_framework.parsers import JSONParser, FileUploadParser


class CollectionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [
        JSONParser,
        FileUploadParser,
    ]

    def get(self, request, *args, **kwargs):
        """
        Return the list of decks, each with name and cards to study/review/etc
        """
        session = request.session
        col = get_collection(session)
        if col is None:
            return JsonResponse(
                {"warn": "No collection found for current user"}, status=200
            )

        deck_list = []
        dueTree = col.sched.deckDueTree()
        for node in dueTree:
            name, did, due, lrn, new, children = node
            if did == 1:
                continue
            sub_deck = []
            for sub_node in children:
                sub_name, sub_did, sub_due, sub_lrn, sub_new, sub_children = sub_node
                sub_deck.append(
                    {
                        "name": sub_name,
                        "did": sub_did,
                        "new": sub_new,
                        "due": sub_due,
                        "lrn": sub_lrn,
                    }
                )
            deck_list.append(
                {
                    "name": name,
                    "did": did,
                    "new": new,
                    "due": due,
                    "lrn": lrn,
                    "sub_deck": sub_deck,
                }
            )
        col.close()
        return JsonResponse({"decks": deck_list}, status=200)

    def put(self, request, *args, **kwargs):
        """
        Upload a collection file
        """
        file_obj = request.data["file"]
        
        return
