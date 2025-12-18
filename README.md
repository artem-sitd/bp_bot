# Telegram Bot — Business Processes Reminder

## 📌 Описание
Простой Telegram-бот для:
- регистрации пользователей,
- отображения закреплённых бизнес-процессов,
- расчёта дедлайнов и напоминаний,
- хранения данных в базе,
- выгрузки процессов в Google Sheets.

Решение намеренно упрощено в рамках тестового задания.

---

## ⚙️ Стек
- Python 3.11
- aiogram 3
- SQLite
- SQLAlchemy
- Google Sheets API (gspread)

---

### 1. Установка зависимостей
```
pip install -r requirements.txt
```

## 🚀 Запуск проекта
- ```git clone https://github.com/artem-sitd/bp_bot.git```
- ```cd bp_bot```
- ```cp .env.example .env```
- заполняем .env вашим токеном, Далее:
- ```pip install -r requirements.txt``` # установка зависимостей
- ```python3 seed.py``` # заполянет БД
- далее необходимо настроить google cloude, дать разрешение на апи, скачать креды
- ```python3 sheets.py``` # заполняет гугл таблицу
- ```python3 bot.py``` или ```python3 -m bot```