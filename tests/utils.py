from aiogram.types import User, Chat, Message
from datetime import datetime

TEST_USER = User(id=123, is_bot=False, first_name='Test',last_name='Bot', username='testbot', language_code='ru-RU')
TEST_USER_CHAT = Chat(id=1236659345, type='private', title=None, username=TEST_USER.username, first_name=TEST_USER.first_name, last_name=TEST_USER.last_name)

def get_message(text:str):
    return Message(message_id=123, date=datetime.now(), chat=TEST_USER_CHAT, from_user=TEST_USER, sender_chat=TEST_USER_CHAT)