from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import config

bot = Bot(config.token)
disp = Dispatcher(bot, storage = MemoryStorage())

@disp.message_handler(text=['Привет!'])
async def send_welcome(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

@disp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Приветствую! Я бот, помогающий тебе учиться!')

@disp.message_handler()
async def all_message(message: types.Message):
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)