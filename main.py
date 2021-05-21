from flask import Flask
from flask import request
from flask import make_response
import pymongo

import settings

app = Flask(__name__)

# establish database connection
database = pymongo.MongoClient(settings.db_host, username=settings.db_user, password=settings.db_pass,
                            port=settings.db_port)


@app.route("/")
def index():
    mydb = database["indicators"]
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
        def insert_indicator(indicator):
            if indicator['exchange'] == 'binance':
                from binance.client import Client
                binance_client = Client(settings.api_key, settings.api_secret)
                binance_ticker = binance_client.get_ticker(symbol=indicator['pair'])
                indicator = {**indicator, **binance_ticker}

            mydb = database["indicators"]
            mycol = mydb["aurox"]
            indicator['remote_addr'] = request.remote_addr
            _id = mycol.insert_one(indicator)

        aurox_indicator = request.get_json()
        if isinstance(aurox_indicator, dict):
            insert_indicator(aurox_indicator)
        elif isinstance(aurox_indicator, list):
            for i in aurox_indicator:
                insert_indicator(i)

        return "success"

    else:
        mydb = database["indicators"]
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
