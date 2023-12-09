import asyncio
from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPRequest
import json
import base64
import datetime
import time

URL = "https://tgloggerbot-hellcat.amvera.io/" # - раскомментить при загрузке на хостинг
#URL = "http://localhost:8080/" # - закомментить при загрузке на хостинг

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

def get_last_log_id(user_id : str, train_id : str) -> str:
    data = {
        "type": "SELECT",
        "what": "log_id",
        "user_id": user_id,
        "train_id": train_id
    }
    prepared = json.dumps(data)
    response = post_request(prepared)
    return response

class Train:
    def __init__(self, user_id) -> None:
        self.train_id = None
        self.time_start = None
        '''data = {
            "type": "SELECT",
            "what": "user_id",
            "user_id": user_id
        }
        prepared = json.dumps(data)
        response = post_request(prepared)
        if response == "ok":
            self.user_id = user_id
        else:
            self.user_id = None
            raise RuntimeError(response)'''
        self.user_id = user_id
    
    def create_train(self) -> str:
        if self.train_id is not None:
            raise RuntimeError("Train is already created.")
        last_id = get_last_train_id(self.user_id)
        try:
            new_id = str(int(last_id) + 1)
        except ValueError:
            new_id = '0'
        self.time_start = str(datetime.datetime.now())
        data = {
            "type": "INSERT",
            "what": "train_status",
            "train_id": new_id,
            "user_id": self.user_id,
            "train_status": "InProgress",
            "time_start": self.time_start,
            "time_end": "-"
        }
        prepared = json.dumps(data)
        response = post_request(prepared)
        self.train_id = new_id
        print(response)
        return new_id

    def send_metrics(self, epoch : int, metric_type : str, metric_score : float):
        if self.train_id is None:
            raise RuntimeError("Train was not created")
        last_id = get_last_log_id(self.user_id, self.train_id)
        try:
            new_id = str(int(last_id) + 1)
        except ValueError:
            new_id = '0'
        metric_time = str(datetime.datetime.now())
        data = {
            "type": "INSERT",
            "what": "logs_table",
            "log_id": new_id,
            "user_id": self.user_id,
            "train_id": self.train_id,
            "epoch": epoch,
            "metric_type": metric_type,
            "metric_score": metric_score,
            "time": metric_time
        }
        prepared = json.dumps(data)
        response = post_request(prepared)
        self.train_id = new_id
        print(response)

    def end_train(self):
        if self.train_id is None:
            raise RuntimeError("Train was not created.")
        time_end = str(datetime.datetime.now())
        data = {
            "type": "UPDATE",
            "what": "train_status",
            "train_id": self.train_id,
            "user_id": self.user_id,
            "train_status": "Finished",
            "time_start": self.time_start,
            "time_end": time_end
        }
        prepared = json.dumps(data)
        response = post_request(prepared)
        self.train_id = None
        self.time_start = None
        print(response)
