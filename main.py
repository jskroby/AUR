from flask import Flask
from flask import request
import json
from binance.client import Client
import secrets
client = Client(secrets.api_key, secrets.api_secret)
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>flask-webhooks main page</p>"


@app.route("/aurox", methods=['POST'])
def aurox_webhook():
    response = request.get_json()
    if response['exchange'] == 'binance':
        with open('data.json', 'a') as outfile:
            json.dump(response, outfile)
            outfile.write('\n')

    return "success"
