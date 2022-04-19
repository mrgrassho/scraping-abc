FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY . .

CMD [ "python3", "./go-spider.py" ]