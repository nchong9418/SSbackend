from flask import Flask, request, jsonify
from flask import CORS
import json

import sqlImplementation
from sqlImplementation import get_item, add_item, update_item, personSignedUp
import redis
import redis_clients 


app = Flask(__name__)
CORS(app) #communicate to frontend 

CARD_CACHE_KEY = "all_study_cards"

#Start implementing routes below

'''
@app.route('/cards', methods=[''])
def function():
    accept data request

    logical check if JSON contains necessary things
        If missing something return error

    implement method logic

    delete cache 

    return card informat like

    return jsonify(new_card),200 or 201

'''

@app.route('/cards', methods=['POST'])
def add_new_card():
        data = request.get_json()
        if not data or 'title' not in data or 'hostname' not in data:
            return jsonify({"error": "Missing fields title or hostname"}), 400 

        #create new card here using function
        #new_card = make_card(data)

        if redis_client:
            redis_client.delete(CARD_CACHE_KEY) #remove cache
        #return jsonify(new_card), 201
        #Uncomment once new_card() is made.