from aiogram import Bot, Dispatcher
from aiogram.types import Message
import random
import asyncio

API_TOKEN = "7848370476:AAFjsPOvNg_YR0h8qY79H0_p4Mc85bU0g5I"  # Замените на токен вашего бота

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

# Изначальный список сотрудников
employees = [f"{i}" for i in range(1, 15)]

# Словарь для хранения распределения очереди
user_queues = {}

@dp.message_handler(commands=['start'])
async def start(message: Message):
    """
    Регистрирует пользователя и раздает уникальный номер в очереди с эффектом ожидания.
    """
    global employees

    # Проверяем, зарегистрирован ли пользователь
    if message.from_user.id in user_queues:
        queue_number = user_queues[message.from_user.id]
        await message.answer(f"Вы уже зарегистрированы! Ваш номер в очереди: {queue_number}.")
    else:
        # Если сотрудники еще остались
        if employees:
            await message.answer("Вы зарегистрировались! Секундочку...")
            await asyncio.sleep(1)  # Пауза перед интригой
            await message.answer("🎲 Барабанная дробь...")
            await asyncio.sleep(2)  # Пауза для интриги

            # Случайно выбираем сотрудника
            assigned_employee = random.choice(employees)
            employees.remove(assigned_employee)  # Убираем из доступных

            # Сохраняем номер для пользователя
            user_queues[message.from_user.id] = assigned_employee
            await message.answer(f"✨ БУМ! Ваш номер в очереди: {assigned_employee}.")
        else:
            await message.answer("Извините, но все места в очереди уже распределены!")

@dp.message_handler(commands=['reset'])
async def reset(message: Message):
    """
    Сбрасывает очередь. Только для администратора.
    """
    admin_id =  6573322342 # Замените на ваш Telegram ID
    global employees, user_queues

    if message.from_user.id == admin_id:
        employees = [f"Сотрудник {i}" for i in range(1, 14)]
        user_queues = {}
        await message.answer("Очередь сброшена. Можно снова распределять номера.")
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

@dp.message_handler(commands=['queue'])
async def queue(message: Message):
    """
    Показывает, какой номер у пользователя.
    """
    if message.from_user.id in user_queues:
        queue_number = user_queues[message.from_user.id]
        await message.answer(f"Ваш номер в очереди: {queue_number}.")
    else:
        await message.answer("Вы еще не зарегистрированы. Введите /start, чтобы получить номер.")

if __name__ == "__main__":
    print("Бот запущен...")
    from aiogram.utils import executor
    executor.start_polling(dp, skip_updates=True)
