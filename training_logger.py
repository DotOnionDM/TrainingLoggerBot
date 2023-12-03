import asyncio
from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPRequest
import json
import base64
import datetime

# URL = "https://tgloggerbot-hellcat.amvera.io/" # - раскомментить при загрузке на хостинг
URL = "http://localhost:8080/" # - закомментить при загрузке на хостинг

def post_request(data):
    http_client = HTTPClient()
    request = HTTPRequest(url=URL, method="POST", body=data)
    response = http_client.fetch(request=request)
    return response.body

def get_last_train_id(user_id : str) -> str:
    data = {
        "type": "SELECT",
        "what": "train_id",
        "user_id": user_id
    }
    prepared = json.dumps(data)
    response = post_request(prepared)
    return response
    

def create_train(user_id) -> str:
    last_id = get_last_train_id(user_id)
    try:
        new_id = str(int(last_id) + 1)
    except ValueError:
        new_id = '0'
    time_start = str(datetime.datetime.now())
    data = {
        "type": "INSERT",
        "what": "train_status",
        "train_id": new_id,
        "user_id": user_id,
        "train_status": "InProgress",
        "time_start": time_start,
        "time_end": "-"
    }
    prepared = json.dumps(data)
    response = post_request(prepared)
    print(response)
    return new_id

def send_metrics():
    pass

def end_train():
    pass
