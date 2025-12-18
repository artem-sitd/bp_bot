# Copyright (c) 2025 Artem Albertov
# All Rights Reserved.
# This code is provided for review purposes only.
# Any unauthorized use is strictly prohibited.

from db import engine, SessionLocal
from models import Base, BusinessProcess

Base.metadata.create_all(bind=engine)

session = SessionLocal()

# Проверка, чтобы не засеивать дважды
exists = session.query(BusinessProcess).first()
if exists:
    print("Бизнес-процессы уже существуют")
    exit()

processes = [
    BusinessProcess(
        name="Заполнить таблицу показателей",
        responsible_name="Кирилл",
        periodicity="ежедневно",
        deadline_time="23:59",
        remind_1_hours=24,
        remind_2_hours=2
    ),
    BusinessProcess(
        name="Посмотреть просмотры конкурентов",
        responsible_name="Кирилл",
        periodicity="ежедневно",
        deadline_time="23:59",
        remind_1_hours=24,
        remind_2_hours=2
    ),
    BusinessProcess(
        name="Заполнить КОПы",
        responsible_name="Иван",
        periodicity="ежедневно",
        deadline_time="10:30",
        remind_1_hours=24,
        remind_2_hours=2
    ),
    BusinessProcess(
        name="Проверить рекламные кампании",
        responsible_name="Иван",
        periodicity="ежедневно",
        deadline_time="12:00",
        remind_1_hours=24,
        remind_2_hours=2
    ),
]

session.add_all(processes)
session.commit()
session.close()

print("Бизнес-процессы успешно добавлены")
