# Copyright (c) 2025 Artem Albertov
# All Rights Reserved.
# This code is provided for review purposes only.
# Any unauthorized use is strictly prohibited.

from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)


class BusinessProcess(Base):
    __tablename__ = "business_processes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    responsible_name = Column(String, nullable=False)
    periodicity = Column(String, nullable=False)
    deadline_time = Column(String, nullable=False)   # "10:30"
    remind_1_hours = Column(Integer, nullable=False)
    remind_2_hours = Column(Integer, nullable=False)
