from aiogram import Bot, Dispatcher, types, F
import sqlite3
import uuid
import pandas as pd


def find_user_id(db, msg_chat_id):
    connection = sqlite3.connect(db)
    query_find_user_id = f"SELECT user_id FROM chat_user_table WHERE chat_id = '{msg_chat_id}'"
    user_id = connection.execute(query_find_user_id).fetchone()
    connection.close()
    return user_id


def insert_user_id(db, msg_chat_id):
    connection = sqlite3.connect(db)
    unique_id = str(uuid.uuid4())
    query_insert_user_id = f"INSERT INTO chat_user_table(chat_id, user_id) VALUES ('{msg_chat_id}', '{unique_id}')"
    connection.execute(query_insert_user_id)
    connection.commit()
    connection.close()
    return [unique_id]


def get_user_id_statistics(db, user_id):
    connection = sqlite3.connect(db)
    query_user_id_statistics = f"SELECT * FROM logs_table WHERE user_id = '{user_id}'"

    query_get_statistics = pd.read_sql_query(query_user_id_statistics, connection)
    data = pd.DataFrame(query_get_statistics,
                        columns=['log_id', 'user_id', 'train_id', 'epoch', 'metric_type', 'metric_score', 'time'])
    connection.close()
    return data.values.tolist()


def get_train_id_statistics(db, train_id):
    connection = sqlite3.connect(db)
    query_train_id_statistics = pd.read_sql_query(f"SELECT * FROM logs_table WHERE train_id = '{train_id}'", connection)
    data = pd.DataFrame(query_train_id_statistics,
                        columns=['log_id', 'user_id', 'train_id', 'epoch', 'metric_type', 'metric_score', 'time'])
    connection.close()
    return data

