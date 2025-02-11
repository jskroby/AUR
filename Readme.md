# aurox signals

Collects the signals from aurox and stores them in a database. Currently supports Price ticker from Binance only. The Webhook url is http://localhost:5001/aurox (adjust port number)
## env files
copy _.env.sample_ to _.env_ and _settings.sample.py_ to _settings.py_ and adjust the settings.

## run with docker and docker-compose
(easy way)

```bash
docker-compose up -d
```
your flask installation is accessible at http://localhost:5001 and the mongo-express at http://localhost:27017

## run with python interpreter
installation requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
start a MongoDB server and adjust the _db_host_ parameter in _settings.py_.

run flask app with
```bash
FLASK_APP=main venv/bin/flask run
```

## run with ngrok
if your installation doesn't run on a public server, e.g. local machine, it's recommended to make the installation accessible via ngrok

Register, download and install [ngrok](https://dashboard.ngrok.com/get-started/setup) and follow the instructions. Ngrok can be started with `./ngrok http 5000` or `./ngrok http 5001` depending on the port opened. 