from flask import Flask
from flask import request
import json
from binance.client import Client

import settings
client = Client(settings.api_key,
                settings.api_secret)
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>flask-webhooks main page</p>"


@app.route("/aurox", methods=['POST'])
def aurox_webhook():
    aurox_indicator = request.get_json()
    if aurox_indicator['exchange'] == 'binance':
        binance_ticker = client.get_ticker(symbol=aurox_indicator['pair'])

        with open('data.json', 'a') as outfile:
            merged = {**aurox_indicator, **binance_ticker}
            json.dump(merged, outfile)
            outfile.write('\n')

    return "success"
