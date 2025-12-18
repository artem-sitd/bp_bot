# Copyright (c) 2025 Artem Albertov
# All Rights Reserved.
# This code is provided for review purposes only.
# Any unauthorized use is strictly prohibited.

import asyncio
import os
from datetime import datetime, time

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from db import SessionLocal
from models import User, BusinessProcess

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# 🔹 /check DD-MM-YYYY HH:MM
@dp.message(Command("check"))
async def check_deadlines(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "Используй формат:\n/check 15-12-2025 09:00"
        )
        return

    try:
        check_dt = datetime.strptime(parts[1], "%d-%m-%Y %H:%M")
    except ValueError:
        await message.answer("Неверный формат даты 😢")
        return

    session = SessionLocal()

    user = session.query(User).filter_by(
        telegram_id=message.from_user.id
    ).first()

    if not user:
        await message.answer("Сначала зарегистрируйся через /start")
        session.close()
        return

    processes = session.query(BusinessProcess).filter_by(
        responsible_name=user.name
    ).all()

    if not processes:
        await message.answer("У тебя нет процессов.")
        session.close()
        return

    text = f"⏰ Проверка на {check_dt.strftime('%d-%m-%Y %H:%M')}\n\n"

    for p in processes:
        deadline_t = datetime.strptime(p.deadline_time, "%H:%M").time()
        deadline_dt = datetime.combine(check_dt.date(), deadline_t)

        delta_hours = (deadline_dt - check_dt).total_seconds() / 3600

        if delta_hours < 0:
            status = "❌ Дедлайн прошёл"
        elif delta_hours <= p.remind_2_hours:
            status = "⚠️ Срочно!"
        elif delta_hours <= p.remind_1_hours:
            status = "🔔 Скоро дедлайн"
        else:
            status = "✅ Пока рано"

        text += (
            f"📌 {p.name}\n"
            f"⏰ Дедлайн: {deadline_dt.strftime('%H:%M')}\n"
            f"📊 Осталось: {delta_hours:.1f} ч\n"
            f"{status}\n\n"
        )

    await message.answer(text)
    session.close()


# 🔹 /my — показать процессы
@dp.message(Command("my"))
async def my_processes(message: Message):
    session = SessionLocal()
    user = session.query(User).filter_by(
        telegram_id=message.from_user.id
    ).first()

    if not user:
        await message.answer("Сначала зарегистрируйся через /start")
        session.close()
        return

    processes = session.query(BusinessProcess).filter_by(
        responsible_name=user.name
    ).all()

    if not processes:
        await message.answer("У тебя нет закреплённых процессов.")
        session.close()
        return

    text = "📋 **Твои бизнес-процессы:**\n\n"
    for p in processes:
        text += (
            f"📌 {p.name}\n"
            f"⏱ {p.periodicity}\n"
            f"⏰ Дедлайн: {p.deadline_time}\n\n"
        )

    await message.answer(text, parse_mode="Markdown")
    session.close()


# 🔹 /start — регистрация
@dp.message(Command("start"))
async def start(message: Message):
    session = SessionLocal()

    user = session.query(User).filter_by(
        telegram_id=message.from_user.id
    ).first()

    if user:
        await message.answer(f"Привет, {user.name}! 👋")
    else:
        await message.answer(
            "Привет! Введи своё имя (как в бизнес-процессах):"
        )

    session.close()


# 🔹 Сохраняем имя (если ещё не зарегистрирован)
@dp.message(F.text & ~F.text.startswith("/"))
async def register_name(message: Message):
    session = SessionLocal()

    user = session.query(User).filter_by(
        telegram_id=message.from_user.id
    ).first()

    if user:
        await message.answer(
            f"{user.name} вы жуе зарегистрированы, список доступных команд бота: /my, /check ДД-ММ-ГГГГ ЧЧ:ММ"
        )
        session.close()
        return

    new_user = User(
        telegram_id=message.from_user.id,
        name=message.text.strip()
    )
    session.add(new_user)
    session.commit()
    session.close()

    await message.answer(
        f"✅ Зарегистрирован как **{new_user.name}**",
        parse_mode="Markdown"
    )


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
