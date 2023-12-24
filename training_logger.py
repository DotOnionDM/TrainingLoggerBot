import uuid
import asyncio
import requests
import json
import base64
import datetime
import time

URL = "https://tgloggerbot-hellcat.amvera.io/" # - раскомментить при загрузке на хостинг
#URL = "http://localhost:8080/" # - закомментить при загрузке на хостинг

def post_request(data):
    response = requests.post(URL, data=data)
    if response.status_code != 200:
        raise RuntimeError(f"Response status is {response.status_code}!")
        exit(1)
    return response.text

class Train:
    def __init__(self, user_id: str) -> None:
        self.train_id = None
        self.num_epochs = None
        self.time_start = None
        data = {
            "type": "SELECT",
            "what": "user_id",
            "user_id": user_id
        }
        prepared = json.dumps(data)
        post_request(prepared)
        self.user_id = user_id
        self.user_id = user_id
    
    def create_train(self, train_id: str = None, num_epochs: int = None) -> str:
        if self.train_id is not None:
            raise RuntimeError("Train is already created.")
        
        if train_id is None:
            new_id = str(uuid.uuid4())
        else:
            new_id = train_id
        
        self.time_start = str(datetime.datetime.now())
        data = {
            "type": "INSERT",
            "what": "train_status",
            "train_id": new_id,
            "user_id": self.user_id,
            "num_epochs": num_epochs,
            "train_status": "InProgress",
            "time_start": self.time_start,
            "time_end": "-"
        }
        prepared = json.dumps(data)
        response = post_request(prepared)
        self.train_id = new_id
        self.num_epochs = num_epochs
        print(response)
        return new_id

    def send_metrics(self, epoch : int, metric_type : str, metric_score : float):
        if self.train_id is None:
            raise RuntimeError("Train was not created")
        
        new_id = str(uuid.uuid4())
        
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
        post_request(prepared)

    def end_train(self):
        if self.train_id is None:
            raise RuntimeError("Train was not created.")
        time_end = str(datetime.datetime.now())
        data = {
            "type": "UPDATE",
            "what": "train_status",
            "train_id": self.train_id,
            "user_id": self.user_id,
            "num_epochs": self.num_epochs,
            "train_status": "Finished",
            "time_start": self.time_start,
            "time_end": time_end
        }
        prepared = json.dumps(data)
        response = post_request(prepared)
        self.train_id = None
        self.time_start = None
        print(response)
