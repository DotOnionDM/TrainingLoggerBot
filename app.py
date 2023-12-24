import uuid
import sqlite3
from sqlite3 import Error
from contextlib import closing
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile
import asyncio
import tornado
import tornado.web
import random
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime
from gigachat import GigaChat

AMVERA_MODE = True
if AMVERA_MODE:
    path = "/data/config.dat"
    db_path = "/data/Logs.db"
else:
    path = "config.dat"
    db_path = "Logs.db"

with open(path, "r") as dat:
    data = dat.read()
    bot_token = data.split("\n")[0]
    giga_token = data.split("\n")[1]
    
TOKEN = bot_token
GIGACHAT_TOKEN = giga_token
database = db_path

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start", "go"))
async def start_handler(message: types.Message):
    unique_id = str(uuid.uuid4())
    query_insert_user_id = f'''
    INSERT INTO users(unique_user_id)
    VALUES ("{unique_id}")
    '''
    connection = sqlite3.connect(database)
    connection.execute(query_insert_user_id)
    connection.commit()
    connection.close()

    builder = ReplyKeyboardBuilder()
    builder.button(text="Хочу мем с попугаем")
    builder.button(text="Хочу график обучения")
    builder.button(text="Хочу время до конца обучения")
    builder.adjust(*[1] * 3)
    markup = builder.as_markup(resize_keyboard = True)

    await bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}! Я бот - логгер процесса обучения нейросетей. Тебе присвоен уникальный id: {unique_id}.", reply_markup = markup)

@dp.message(F.text.startswith('График обучения: '))
async def plot_training(message: types.Message):
    text = message.text.lower()
    text = text[17:]
    chat_id = message.chat.id

    connection = sqlite3.connect(database)

    query_get_info = pd.read_sql_query(f'''
        SELECT * FROM logs_table
        WHERE train_id = "{text}"
        ''', connection)

    data = pd.DataFrame(query_get_info, columns = ['log_id', 'user_id', 'train_id', 'epoch', 'metric_type', 'metric_score', 'time'])
    connection.close()

    builder = ReplyKeyboardBuilder()
    builder.button(text="Хочу мем с попугаем")
    builder.button(text="Хочу график обучения")
    builder.button(text="Хочу время до конца обучения")
    builder.adjust(*[1] * 3)
    markup = builder.as_markup(resize_keyboard = True)

    if data.empty:
        await bot.send_message(chat_id, 'Что-то пошло не так. Может, опечатка в названии модели? Попробуй еще раз!', reply_markup = markup)
    else:
        data.sort_values(by = ['epoch'])
        x = data['epoch'].to_numpy()
        y = data['metric_score'].to_numpy()
        sns.set(style='darkgrid', palette='deep')
        plt.figure(figsize = (10, 7))
        plt.plot(x, y, linestyle = '--', linewidth = 3, marker = 'o', markersize = 10)
        title = "График зависимости " + data['metric_type'][0] + " от эпохи\n"
        plt.title(title, fontsize = 15)
        plt.xlabel("Эпоха", fontsize = 15)
        ylabel = "\nЗначение " + data['metric_type'][0] + "\n"
        plt.ylabel(ylabel, fontsize = 15)
        plt.xticks(np.arange(min(data['epoch'].to_numpy()), max(data['epoch'].to_numpy()) + 1, 1))
        plt.savefig('figure.png')
        await bot.send_message(chat_id, 'Лови!', reply_markup = markup)
        figure = FSInputFile("figure.png")
        await bot.send_document(message.chat.id, figure, reply_markup = markup)

@dp.message(F.text.startswith('Время до конца обучения: '))
async def plot_training(message: types.Message):
    text = message.text.lower()
    text = text[25:]
    chat_id = message.chat.id

    connection = sqlite3.connect(database)

    query_get_info = pd.read_sql_query(f'''
        SELECT * FROM logs_table
        WHERE train_id = "{text}"
        ''', connection)

    data = pd.DataFrame(query_get_info, columns = ['log_id', 'user_id', 'train_id', 'epoch', 'metric_type', 'metric_score', 'time'])
    connection.close()

    builder = ReplyKeyboardBuilder()
    builder.button(text="Хочу мем с попугаем")
    builder.button(text="Хочу график обучения")
    builder.button(text="Хочу время до конца обучения")
    builder.adjust(*[1] * 3)
    markup = builder.as_markup(resize_keyboard = True)

    if data.empty:
        await bot.send_message(chat_id, 'Что-то пошло не так. Может, опечатка в названии модели? Попробуй еще раз!', reply_markup = markup)
    else:
        data.sort_values(by = ['epoch'], ascending = [False])
        connection = sqlite3.connect(database)
        query_get_info = pd.read_sql_query(f'''
            SELECT * FROM status_table
            WHERE train_id = "{text}"
            ''', connection)
        data_status = pd.DataFrame(query_get_info, columns = ['train_id', 'user_id', 'num_epochs', 'train_status', 'metric_type', 'time_start', 'time_end'])
        connection.close()
        current_train_status = data_status['train_status'].iloc[0]

        if current_train_status == "Finished":
            await bot.send_message(chat_id, 'Эта модель уже закончила обучение!', reply_markup = markup)

        else:
            last_log_epoch = data['epoch'].iloc[0]
            last_log_time = data['time'].iloc[0]
            num_epoch = data_status['num_epochs'].iloc[0]
            start_time = data_status['time_start'].iloc[0]
    
            datetime_last_log_time = datetime.datetime.strptime(last_log_time[:-7], '%Y-%m-%d %H:%M:%S')
            datetime_start_time = datetime.datetime.strptime(start_time[:-7], '%Y-%m-%d %H:%M:%S')
            time_spent = (datetime_last_log_time - datetime_start_time).total_seconds()
            average_time_epoch = time_spent / last_log_epoch
            epochs_left = num_epoch - last_log_epoch
            calculated_time_end = average_time_epoch * epochs_left
            calc_hours = calculated_time_end // 3600
            calc_minutes = (calculated_time_end - calc_hours * 3600) // 60
            calc_seconds = (calculated_time_end - calc_hours * 3600 - calc_minutes * 60)

            await bot.send_message(chat_id, f'До конца обучения осталось приблизительно "{calc_hours}" часов, "{calc_minutes}" минут, "{calc_seconds}" секунд.\nЕсли хотите получить уведомление примерно через это время, чтобы проверить, завершила ли модель обучение, напишите "Хочу уведомление о train_id" без кавычек, train_id – название модели, слово "Хочу" с большой буквы', reply_markup = markup)


@dp.message(F.text.startswith('Хочу уведомление о '))
async def plot_training(message: types.Message):
    text = message.text.lower()
    text = text[19:]
    chat_id = message.chat.id

    connection = sqlite3.connect(database)

    query_get_info = pd.read_sql_query(f'''
        SELECT * FROM logs_table
        WHERE train_id = "{text}"
        ''', connection)

    data = pd.DataFrame(query_get_info, columns = ['log_id', 'user_id', 'train_id', 'epoch', 'metric_type', 'metric_score', 'time'])
    connection.close()

    data.sort_values(by = ['epoch'], ascending = [False])
    connection = sqlite3.connect(database)
    query_get_info = pd.read_sql_query(f'''
        SELECT * FROM status_table
        WHERE train_id = "{text}"
        ''', connection)
    data_status = pd.DataFrame(query_get_info, columns = ['train_id', 'user_id', 'num_epochs', 'train_status', 'metric_type', 'time_start', 'time_end'])
    connection.close()
    current_train_status = data_status['train_status'].iloc[0]

    last_log_epoch = data['epoch'].iloc[0]
    last_log_time = data['time'].iloc[0]
    num_epoch = data_status['num_epochs'].iloc[0]
    start_time = data_status['time_start'].iloc[0]
    
    datetime_last_log_time = datetime.datetime.strptime(last_log_time[:-7], '%Y-%m-%d %H:%M:%S')
    datetime_start_time = datetime.datetime.strptime(start_time[:-7], '%Y-%m-%d %H:%M:%S')
    time_spent = (datetime_last_log_time - datetime_start_time).total_seconds()
    average_time_epoch = time_spent / last_log_epoch
    epochs_left = num_epoch - last_log_epoch
    calculated_time_end = average_time_epoch * epochs_left

    builder = ReplyKeyboardBuilder()
    builder.button(text="Хочу мем с попугаем")
    builder.button(text="Хочу график обучения")
    builder.button(text="Хочу время до конца обучения")
    builder.adjust(*[1] * 3)
    markup = builder.as_markup(resize_keyboard = True)

    await bot.send_message(chat_id, f'Зафиксировал. Уведомление будет!', reply_markup = markup)
    await asyncio.sleep(calculated_time_end)
    await bot.send_message(chat_id, f'О, возможно, модель {text} уже завершила обучение. Можете проверить, сколько времени осталось до конца', reply_markup = markup)


@dp.message(F.content_type.in_({'text'}))
async def text_handler(message: types.Message):
    text = message.text.lower()
    chat_id = message.chat.id

    builder = ReplyKeyboardBuilder()
    builder.button(text="Хочу мем с попугаем")
    builder.button(text="Хочу график обучения")
    builder.button(text="Хочу время до конца обучения")
    builder.adjust(*[1] * 3)
    markup = builder.as_markup(resize_keyboard = True)

    if text == "хочу мем с попугаем":
        number_meme = random.randint(0, 3)
        connection = sqlite3.connect(database)
        our_cursor = connection.cursor()
        query_get_meme = f'''
        SELECT meme_link FROM images
        WHERE id = "{number_meme}"
        '''
        our_cursor.execute(query_get_meme)
        result = our_cursor.fetchone()
        connection.close()
        if result:
            await bot.send_photo(chat_id, result[0], reply_markup = markup)

    elif text == "хочу график обучения":
        await bot.send_message(chat_id, 'Пожалуйста, отправь название модели, которое было придумано в начале обучения в формате "График обучения: train_id" без кавычек (слово "График" с большой буквы), где train_id – название модели', reply_markup = markup)
    
    elif text == "хочу время до конца обучения":
        await bot.send_message(chat_id, 'Пожалуйста, отправь название модели, которое было придумано в начале обучения в формате "Время до конца обучения: train_id" без кавычек (слово "Время" с большой буквы), где train_id – название модели', reply_markup = markup)

    else:
        with GigaChat(credentials=GIGACHAT_TOKEN, verify_ssl_certs=False) as giga:
            response = giga.chat(f"Ты - бот-ассистент в программе, которая помогает пользователям записывать результаты обучения нейросетей и отвечать на другие вопросы пользователя. Пользователь задает тебе вопрос: {text}")
        ans = response.choices[0].message.content
        ans += "\n \nДанное сообщение было сгенерировано Gigachat"
        await bot.send_message(chat_id, ans, reply_markup = markup)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.send_error(status_code=405)

    def post(self):
        data = json.loads(self.request.body)
        try:
            if (data["type"] == "SELECT") and (data["what"] == "user_id"):
                query_get_user_id = f'''
                SELECT user_id FROM chat_user_table
                WHERE user_id = "{data["user_id"]}"
                '''
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                cursor.execute(query_get_user_id)
                result = cursor.fetchone()
                connection.close()
                if not result:
                    self.send_error(status_code=404)
                else:
                    self.set_status(status_code=200)
            elif (data["type"] == "INSERT") and (data["what"] == "train_status"):
                try:
                    num = int(data["num_epochs"])
                except TypeError:
                    self.send_error(403)
                query_insert_train = f'''
                INSERT INTO status_table(train_id, user_id, num_epochs, train_status, time_start, time_end)
                VALUES ("{data["train_id"]}", "{data["user_id"]}",
                {data["num_epochs"]}, "{data["train_status"]}",
                "{data["time_start"]}", "{data["time_end"]}")
                '''
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                cursor.execute(query_insert_train)
                connection.commit()
                connection.close()
                self.write("Train created")
            elif (data["type"] == "UPDATE") and (data["what"] == "train_status"):
                try:
                    num = int(data["num_epochs"])
                except TypeError:
                    self.send_error(403)
                query_update_train = f'''
                UPDATE status_table
                SET time_end = "{data["time_end"]}", train_status = "{data["train_status"]}"
                WHERE user_id = "{data["user_id"]}" AND train_id = "{data["train_id"]}"
                '''
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                cursor.execute(query_update_train)
                connection.commit()
                connection.close()
                self.write("Train ended")
            elif (data["type"] == "INSERT") and (data["what"] == "logs_table"):
                try:
                    num = int(data["epoch"])
                except TypeError:
                    self.send_error(403)
                query_insert_log = f'''
                INSERT INTO logs_table(log_id, user_id, train_id, epoch, metric_type, metric_score, time)
                VALUES ("{data["log_id"]}", "{data["user_id"]}",
                "{data["train_id"]}", {data["epoch"]}, "{data["metric_type"]}",
                {data["metric_score"]}, "{data["time"]}")
                '''
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                cursor.execute(query_insert_log)
                connection.commit()
                connection.close()
                self.write("Logs have been added to the database")
            else:
                self.send_error(status_code=503)
        except KeyError:
            self.send_error(status_code=503)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8080)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
