from flask import Flask, request, make_response, render_template
import pymongo

import settings
import filters

app = Flask(__name__)

# establish database connection
database = pymongo.MongoClient(settings.db_host, username=settings.db_user, password=settings.db_pass,
                               port=settings.db_port)

app.jinja_env.filters['float'] = filters.float_filter
app.jinja_env.filters['timestamp'] = filters.timestamp_filter


@app.route("/")
def index():
    mydb = database["indicators"]
    mycol = mydb["aurox"]
    pairs = list(mycol.distinct('pair'))
    return render_template('index.html', pairs=pairs)


@app.route("/aurox", methods=['POST'])
def aurox_webhook():
    if request.remote_addr in settings.whitelist:
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


@app.route("/pair/<name>", methods=['GET'])
def view_pair(name):
    time_unit = request.args.get('time_unit', '')
    mydb = database["indicators"]
    mycol = mydb["aurox"]

    query_params = {
        'pair': name.upper(),
    }
    if time_unit:
        query_params['timeUnit'] = time_unit

    data = list(mycol.find(query_params, {'_id': False}))
    all_pairs = list(mycol.find().distinct('pair'))
    return render_template('pair.html', data=data, pair=name, time_unit=time_unit, all_pairs=all_pairs)


@app.route("/download/<name>", methods=['GET'])
def download(name):
    query_params = {}
    if name.upper() != "ALL":
        query_params['pair'] = name.upper()

    time_unit = request.args.get('time_unit', '')
    if time_unit:
        query_params['timeUnit'] = time_unit

    mydb = database["indicators"]
    mycol = mydb["aurox"]

    first = True
    csv_data = []
    for x in mycol.find(query_params, {'_id': False}):
        keys, values = zip(*x.items())
        if first:
            csv_data.append(';'.join(keys))

        csv_data.append(';'.join(str(v) for v in values))
        first = False
    output = make_response("\n".join(csv_data))
    output.headers["Content-Disposition"] = "attachment; filename=aurox.csv"
    output.headers["Content-type"] = "text/csv"
    return output
