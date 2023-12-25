import sqlite3
import uuid

import pandas as pd


def get_user_id(db, msg_chat_id):
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


def get_train_id_logs_statistics(db, train_id):
    connection = sqlite3.connect(db)
    query_train_id_logs_statistics = pd.read_sql_query(f"SELECT * FROM logs_table WHERE train_id = '{train_id}'",
                                                       connection)
    data = pd.DataFrame(query_train_id_logs_statistics,
                        columns=['log_id', 'user_id', 'train_id', 'epoch', 'metric_type', 'metric_score', 'time'])
    connection.close()
    return data


def get_train_id_status(db, train_id):
    connection = sqlite3.connect(db)
    query_train_id_status = pd.read_sql_query(f"SELECT * FROM status_table WHERE train_id = '{train_id}'", connection)
    data = pd.DataFrame(query_train_id_status,
                        columns=['train_id', 'user_id', 'num_epochs', 'train_status', 'metric_type', 'time_start',
                                 'time_end'])
    connection.close()
    return data


def get_meme(db, number_meme):
    connection = sqlite3.connect(db)
    our_cursor = connection.cursor()
    query_get_meme = f"SELECT meme_link FROM images WHERE id = '{number_meme}'"
    our_cursor.execute(query_get_meme)
    result = our_cursor.fetchone()
    connection.close()
    return result


def insert_train(db, data):
    connection = sqlite3.connect(db)
    unique_id = str(uuid.uuid4())
    query_insert_train = f'''
    INSERT INTO status_table(train_id, user_id, num_epochs, train_status, time_start, time_end)
    VALUES ("{data["train_id"]}", "{data["user_id"]}",
             {data["num_epochs"]}, "{data["train_status"]}",
            "{data["time_start"]}", "{data["time_end"]}")
    '''
    connection.execute(query_insert_train)
    connection.commit()
    connection.close()


def update_train(db, data):
    connection = sqlite3.connect(db)
    unique_id = str(uuid.uuid4())
    query_update_train = f'''
    UPDATE status_table
    SET time_end = "{data["time_end"]}", train_status = "{data["train_status"]}"
    WHERE user_id = "{data["user_id"]}" AND train_id = "{data["train_id"]}"
    '''
    connection.execute(query_update_train)
    connection.commit()
    connection.close()


def insert_logs(db, data):
    connection = sqlite3.connect(db)
    unique_id = str(uuid.uuid4())
    query_insert_logs = f'''
    INSERT INTO logs_table(log_id, user_id, train_id, epoch, metric_type, metric_score, time)
                VALUES ("{data["log_id"]}", "{data["user_id"]}",
                "{data["train_id"]}", {data["epoch"]}, "{data["metric_type"]}",
                {data["metric_score"]}, "{data["time"]}")
    '''
    connection.execute(query_insert_logs)
    connection.commit()
    connection.close()
