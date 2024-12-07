from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
import config
import re

bot = Bot(config.token)
disp = Dispatcher(bot, storage = MemoryStorage())

# Выделяет число из строки со словами.
# Например, из строки "мне 20 лет" - функция вернет число 20
def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@disp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('Доброго дня! Я бот, помогающий Вашему здоровью.\nВведите "Calories", чтобы начать рассчет Вашей нормы калорий.')

@disp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Пожалуйста, введите свой возраст:')
    await UserState.age.set()

@disp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    check_age = extract_number(message.text)
    if not check_age or not (10 <= check_age <= 120):
        await message.reply('Пожалуйста, введите корректный возраст (число от 1 до 120).')
        return
    await state.update_data(age=check_age)
    await message.answer('Пожалуйста, введите свой рост:')
    await UserState.growth.set()

@disp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    check_growth = extract_number(message.text)
    if not check_growth or not (20 <= check_growth <= 250):
        await message.reply('Пожалуйста, введите корректный рост в см (число от 20 до 250).')
        return
    await state.update_data(growth=check_growth)
    await message.answer('Пожалуйста, введите свой вес:')
    await UserState.weight.set()

@disp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    check_weight = extract_number(message.text)
    if not check_weight or not (1 <= check_weight <= 150):
        await message.reply('Пожалуйста, введите корректный вес в кг (число от 1 до 150).')
        return
    await state.update_data(weight=check_weight)
    data = await state.get_data()
    # Упрощенный вариант формулы Миффлина-Сан Жеора: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5
    counter = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] + 5
    await message.answer(f'Ваша норма калорий (по упрощенному варианту формулы Миффлина-Сан Жеора): {counter}.')
    await state.finish()

# Эхо
@disp.message_handler()
async def all_message(message: types.Message):
    await message.answer(message.text + ' ' + 'Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)