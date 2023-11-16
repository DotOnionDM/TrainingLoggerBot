import telebot
import uuid
import sqlite3
from sqlite3 import Error
import base64
from contextlib import closing
from telebot import types

TOKEN = "6741560844:AAGbM3Edwx-92LPynYdBSPU_JXGwT90ct3w"
bot = telebot.TeleBot(TOKEN)
database = 'Logs.db'

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    unique_id = str(uuid.uuid4())
    query_insert_user_id = f'''
    INSERT INTO users(unique_user_id)
    VALUES ("{unique_id}")
    '''
    connection = sqlite3.connect(database)
    connection.execute(query_insert_user_id)
    connection.commit()
    connection.close()
    bot.send_message(message.chat.id, f'Привет, я бот - логгер процесса обучения нейросетей. Тебе присвоен уникальный id: {unique_id}.')

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Привет, я бот - логгер обучения нейросетей. Пока я ничего не умею, но это скоро изменится!')


def main() -> None:
    bot.polling()

if __name__ == "__main__":
    main()
    