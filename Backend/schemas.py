#schemas.py
from pydantic import BaseModel
from typing import Optional 
from datetime import datetime
from enum import Enum
from models import TaskStatus

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserSchema(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    coins: int = None
    points: int = None
    role: Role 

    class Config:
        from_attributes = True  # Ранее orm_mode

class AllowedUserSchema(BaseModel):
    id: int
    telegram_id: int

    class Config:
        from_attributes = True


class UpdatePointsRequest(BaseModel):
    telegram_id: int
    points: int


class SendCoinRequest(BaseModel):
    telegram_id: int
    coins: int

class TaskCreate(BaseModel):
    description: str
    points: int
    coins: int
    deadline: datetime  # Дата дедлайна
    user_id: int        # ID пользователя, создавшего задачу
    status: TaskStatus = TaskStatus.IN_PROGRESS

class TaskSchema(BaseModel):
    id: int
    description: str
    points: int
    coins: int
    deadline: datetime
    user_id: int
    status: TaskStatus

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str  # Название продукта
    coins: int  # Стоимость в монетах

class ProductSchema(BaseModel):
    id: int
    name: str
    coins: int

    class Config:
        from_attributes = True


# Добавляем модель для ответа лидерборда
class LeaderboardUser(BaseModel):
    id: int
    name: str
    level: int
    points: int
    avatar: str | None = None

    class Config:
        from_attributes = True