from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import config

bot = Bot(config.token)
disp = Dispatcher(bot, storage = MemoryStorage())

@disp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    print('Привет! Я бот помогающий твоему здоровью.')

@disp.message_handler()
async def all_message(message: types.Message):
    print('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
