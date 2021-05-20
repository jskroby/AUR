from flask import Flask
from flask import request
import json
from binance.client import Client
import pymongo

import settings
client = Client(settings.api_key,
                settings.api_secret)
app = Flask(__name__)
mongo = pymongo.MongoClient(settings.db_host, username=settings.db_user, password=settings.db_pass)

@app.route("/")
def hello_world():
    return "<p>flask-webhooks main page</p>"


@app.route("/aurox", methods=['POST'])
def aurox_webhook():
    aurox_indicator = request.get_json()
    if aurox_indicator['exchange'] == 'binance':
        binance_ticker = client.get_ticker(symbol=aurox_indicator['pair'])
        merged = {**aurox_indicator, **binance_ticker}

        mydb = mongo["indicators"]
        mycol = mydb["aurox"]
        x = mycol.insert_one(merged)

    return "success"
