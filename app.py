import uuid
import sqlite3
from sqlite3 import Error
from contextlib import closing
from aiogram import Bot, Dispatcher, types, F
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

TOKEN = "TOKEN"
database = '/data/Logs.db'
#database = 'Logs.db'

# MAKE BOT
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

    button_meme = types.KeyboardButton(text="Хочу мем с попугаем")
    button_graph = types.KeyboardButton(text="Хочу график обучения")
    markup = types.ReplyKeyboardMarkup(keyboard=[[button_meme, button_graph]], resize_keyboard=True)

    await bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}! Я бот - логгер процесса обучения нейросетей. Тебе присвоен уникальный id: {unique_id}.", reply_markup = markup)

@dp.message(F.text.startswith('Обучение: '))
async def plot_training(message: types.Message):
    text = message.text.lower()
    text = text[10:]
    chat_id = message.chat.id

    connection = sqlite3.connect(database)

    query_get_info = pd.read_sql_query(f'''
        SELECT * FROM logs_table
        WHERE train_id = "{text}"
        ''', connection)

    data = pd.DataFrame(query_get_info, columns = ['log_id', 'user_id', 'train_id', 'epoch', 'metric_type', 'metric_score', 'time'])
    connection.close()

    button_meme = types.KeyboardButton(text="Хочу мем с попугаем")
    button_graph = types.KeyboardButton(text="Хочу график обучения")
    markup = types.ReplyKeyboardMarkup(keyboard=[[button_meme, button_graph]], resize_keyboard=True)

    if data.empty:
        await bot.send_message(chat_id, 'Что-то пошло не так. Может, опечатка в названии модели? Попробуй еще раз!', reply_markup = markup)
    else:
        data.sort_values(by = ['epoch'])
        x = data['epoch'].to_numpy()
        y = data['metric_score'].to_numpy()
        fig, ax = plt.subplots(nrows = 1, ncols = 1)
        ax.plot(x, y)
        ax.grid()
        title = "График зависимости " + data['metric_type'][0] + " от эпохи"
        plt.title(title)
        plt.xlabel("Эпоха")
        ylabel = "Значение " + data['metric_type'][0]
        plt.ylabel(ylabel)
        plt.xticks(np.arange(min(x), max(x) + 1, 1))
        plt.savefig('figure.png')
        await bot.send_message(chat_id, 'Лови!', reply_markup = markup)
        figure = FSInputFile("figure.png")
        await bot.send_document(message.chat.id, figure, reply_markup = markup)
        plt.close(fig)


@dp.message(F.content_type.in_({'text'}))
async def text_handler(message: types.Message):
    text = message.text.lower()
    chat_id = message.chat.id

    button_meme = types.KeyboardButton(text="Хочу мем с попугаем")
    button_graph = types.KeyboardButton(text="Хочу график обучения")
    markup = types.ReplyKeyboardMarkup(keyboard=[[button_meme, button_graph]], resize_keyboard=True)
    
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
        await bot.send_message(chat_id, 'Пожалуйста, отправь название модели, которое было придумано в начале обучения в формате "Обучение: train_id" без кавычек (слово "Обучение" с большой буквы), где train_id – название модели', reply_markup = markup)

    else:
        await bot.send_message(chat_id, 'К сожалению, я не понимаю, что нужно сделать :(', reply_markup = markup)



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
                    print(result)
                    self.write("User not found")
                else:
                    self.write("ok")
            elif (data["type"] == "INSERT") and (data["what"] == "train_status"):
                query_insert_train = f'''
                INSERT INTO status_table(train_id, user_id, train_status, time_start, time_end)
                VALUES ("{data["train_id"]}", "{data["user_id"]}", "{data["train_status"]}", "{data["time_start"]}", "{data["time_end"]}")
                '''
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                cursor.execute(query_insert_train)
                connection.commit()
                connection.close()
                self.write("Train created")
            elif (data["type"] == "UPDATE") and (data["what"] == "train_status"):
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
                query_insert_log = f'''
                INSERT INTO logs_table(log_id, user_id, train_id, epoch, metric_type, metric_score, time)
                VALUES ("{data["log_id"]}", "{data["user_id"]}", "{data["train_id"]}", {data["epoch"]}, "{data["metric_type"]}", {data["metric_score"]}, "{data["time"]}")
                '''
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                cursor.execute(query_insert_log)
                connection.commit()
                connection.close()
                self.write("Logs have added to database")
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
