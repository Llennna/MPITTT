# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base  # Импортируем Base из base.py

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Импортируем модели после определения Base
from models import User, AllowedUser  # Теперь это безопасно, так как Base уже определен

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)