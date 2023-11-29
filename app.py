import telebot
import uuid
import sqlite3
from sqlite3 import Error
import base64
from contextlib import closing
from telebot import types
import random
import socket

PORT = 80

def server():
    sock = socket.socket()
    data = ""
    sock.bind(('', PORT))
    while data != "fin":
        sock.listen(1)
        conn, addr = sock.accept()
        print("Connected: ", addr)
        data = conn.recv(1024).decode()
        conn.close()
    sock.close()

TOKEN = "6741560844:AAGbM3Edwx-92LPynYdBSPU_JXGwT90ct3w"
database = 'Logs.db'
bot = telebot.TeleBot(TOKEN)

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

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_meme = types.KeyboardButton("Хочу мем с попугаем")
    markup.add(button_meme)

    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}! Я бот - логгер процесса обучения нейросетей. Тебе присвоен уникальный id: {unique_id}.", reply_markup = markup)

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_meme = types.KeyboardButton("Хочу мем с попугаем")
    markup.add(button_meme)
    
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
        if result:
            bot.send_photo(chat_id, result[0], reply_markup = markup)

    else:
        bot.send_message(chat_id, 'Привет, я бот - логгер обучения нейросетей. Пока я ничего не умею, но это скоро изменится!', reply_markup = markup)


def main() -> None:
    bot.polling()

from multiprocessing import Process

if __name__ == "__main__":
    server_proc = Process(target=server)
    server_proc.start()
    main()
    server_proc.join()
