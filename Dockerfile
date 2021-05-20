FROM python:rc-alpine
RUN apk add build-base
COPY requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt

WORKDIR /opt
COPY . .

ENV FLASK_APP=main
ENV FLASK_DEBUG=0
CMD  ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
