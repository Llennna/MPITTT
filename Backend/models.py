# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey   
from base import Base  # Импортируем Base из base.py
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import Enum


class Role(str, PyEnum):
    ADMIN = "admin"
    USER = "user"

class TaskStatus(str, PyEnum):
    IN_PROGRESS = "В процессе"
    ON_REVIEW = "На проверке"
    COMPLETED = "Сделано"
    FAILED = "Провалено"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    points = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    role = Column(Enum(Role), default=Role.USER)

    # Связь с задачами
    tasks = relationship("Task", back_populates="user")


class AllowedUser(Base):
    __tablename__ = "allowed_users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    is_allowed = Column(Boolean, default=False)



class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)  # Описание задачи
    points = Column(Integer, nullable=False)      # Баллы за задачу
    coins = Column(Integer, nullable=False)       # Монеты за задачу
    deadline = Column(DateTime, nullable=False)   # Дедлайн задачи
    status = Column(Enum(TaskStatus), default=TaskStatus.IN_PROGRESS)  # Статус задачи
    user_id = Column(Integer, ForeignKey("users.id"))  # Пользователь, создавший задачу
    
    # Связь с пользователем
    user = relationship("User", back_populates="tasks")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название продукта
    coins = Column(Integer, nullable=False)  # Стоимость в монетах