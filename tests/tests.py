from unittest.mock import AsyncMock
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types, F
from utils import TEST_USER, TEST_USER_CHAT, get_message

import pytest
import asyncio
import inspect

pytest_plugins = ('pytest_asyncio',)

from app import start_handler
from app import text_handler
from app import plot_training


def asyncio_run(async_func):
    def wrapper(*args, **kwargs):
        return asyncio.run(async_func(*args, **kwargs))

    wrapper.__signature__ = inspect.signature(async_func)  # without this, fixtures are not injected
    return wrapper


@asyncio_run
async def test_start_handler():
    message = AsyncMock()
    message.chat.id = '1236659345'
    res = await start_handler(message)
    assert isinstance(res, Bot.send_message)


@asyncio_run
async def test_text_handler_1():
    message = AsyncMock()
    message.text = "хочу мем с попугаем"
    message.chat.id = '1236659345'
    res = await text_handler(message)
    assert isinstance(res, Bot.send_message)


@asyncio_run
async def test_text_handler_2():
    message = AsyncMock()
    message.text = "хочу время до конца обучения"
    message.chat.id = '1236659345'
    res = await text_handler(message)
    assert res.text == 'Пожалуйста, отправь название модели, которое было придумано в начале обучения в формате "Время до конца обучения: train_id" без кавычек (слово "Время" с большой буквы), где train_id – название модели'


@asyncio_run
async def test_text_handler_3():
    message = AsyncMock()
    message.text = "хочу график обучения"
    message.chat.id = '1236659345'
    res = await text_handler(message)
    assert res.text == 'Пожалуйста, отправь название модели, которое было придумано в начале обучения в формате "График обучения: train_id" без кавычек (слово "График" с большой буквы), где train_id – название модели'


@asyncio_run
async def test_text_handler_4():
    message = AsyncMock()
    message.text = "привет"
    message.chat.id = '1236659345'
    res = await text_handler(message)
    assert res.text[len(res.text)-9:] == "Gigachat"


@asyncio_run
async def test_plot_time():
    message = AsyncMock()
    message.text = "Хочу уведомление о "
    message.chat.id = '1236659345'
    res = await plot_training(message)
    assert res.text[len(res.text)-9:] == "Зафиксировал. Уведомление будет!"


asyncio_run(test_start_handler())
asyncio_run(test_text_handler_1())
asyncio_run(test_text_handler_2())
asyncio_run(test_text_handler_3())
asyncio_run(test_text_handler_4())
asyncio_run(test_plot_time())
