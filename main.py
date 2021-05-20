from flask import Flask
from flask import request
from flask import make_response
from binance.client import Client
import pymongo

import settings

# binance client
client = Client(settings.api_key,
                settings.api_secret)

app = Flask(__name__)

# establish database connection
mongo = pymongo.MongoClient(settings.db_host, username=settings.db_user, password=settings.db_pass,
                            port=settings.db_port)


@app.route("/")
def index():
    mydb = mongo["indicators"]
    mycol = mydb["aurox"]

    table_start = "<table border=1><thead>"
    table_end = "</tbody></table>"
    button = "<p><form action='aurox'><input type='submit' value='Download' /></form></p>"
    table_data = []
    first = True

    for x in mycol.find({}, {'_id': False}):
        keys = ['timestampIso', 'pair', 'signal', 'timeUnit', 'confirmed', 'bidPrice', 'askPrice']
        filtered = {key: x[key] for key in keys}
        keys, values = zip(*filtered.items())

        if first:
            table_data.append('<tr><th>' + '</th><th>'.join(keys) + '</th></tr></thead><tbody>')
        table_data.append('<tr><td>' + '</td><td>'.join(values) + '</td></tr>')
        first = False

    return table_start + ''.join(table_data) + table_end + button


@app.route("/aurox", methods=['POST', 'GET'])
def aurox_webhook():
    if request.method == 'POST':

        aurox_indicator = request.get_json()
        if aurox_indicator['exchange'] == 'binance':
            binance_ticker = client.get_ticker(symbol=aurox_indicator['pair'])
            merged = {**aurox_indicator, **binance_ticker}

            mydb = mongo["indicators"]
            mycol = mydb["aurox"]
            x = mycol.insert_one(merged)
        return "success"

    else:
        mydb = mongo["indicators"]
        mycol = mydb["aurox"]
        first = True
        csv_data = []
        for x in mycol.find({}, {'_id': False}):
            keys, values = zip(*x.items())
            if first:
                csv_data.append(';'.join(keys))

            csv_data.append(';'.join(str(v) for v in values))
            first = False
        output = make_response("\n".join(csv_data))
        output.headers["Content-Disposition"] = "attachment; filename=aurox.csv"
        output.headers["Content-type"] = "text/csv"
        return output
