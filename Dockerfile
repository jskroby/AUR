FROM python:rc-alpine
RUN apk add build-base
COPY requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt

WORKDIR /opt
COPY . .
EXPOSE 5000/tcp
CMD  ["gunicorn", "main:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:5000"]
