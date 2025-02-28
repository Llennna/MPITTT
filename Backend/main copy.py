from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from models import User, AllowedUser , Task, Product
from database import SessionLocal, engine, Base
from schemas import UserSchema, AllowedUser Schema, UpdatePointsRequest, ProductCreate, ProductSchema, TaskSchema, TaskCreate
import hashlib
import hmac
import httpx
from fastapi.middleware.cors import CORSMiddleware
from bot import TelegramBot  # Импортируем класс TelegramBot
import threading

class App:
    def __init__(self):
        self.app = FastAPI()
        self.setup_cors()
        self.setup_database()
        self.setup_routes()

        # Создаем и запускаем Telegram бота
        self.bot = TelegramBot("7217254061:AAEzRMDI0CVS09eAydyRyGMbJjzAZqAGpg4")
        threading.Thread(target=self.bot.run, daemon=True).start()  # Запускаем бота в отдельном потоке

    def setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def setup_database(self):
        Base.metadata.create_all(bind=engine)

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def setup_routes(self):
        @self.app.post("/auth/telegram")
        async def auth_telegram(request: Request):
            data = await request.json()
            init_data = data.get("initData")

            if not init_data:
                raise HTTPException(status_code=400, detail="Данные инициализации отсутствуют")

            # Ваша логика валидации и авторизации через Telegram
            # ...

        @self.app.post("/register", response_model=AllowedUser Schema)
        def register_user(telegram_id: int, db: Session = Depends(self.get_db)):
            existing_user = db.query(AllowedUser ).filter(AllowedUser .telegram_id == telegram_id).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Пользователь уже добавлен")

            new_allowed_user = AllowedUser (telegram_id=telegram_id)
            db.add(new_allowed_user)
            db.commit()
            db.refresh(new_allowed_user)

            return new_allowed_user

        @self.app.post("/start", response_model=User Schema)
        def start_registration(telegram_id: int, username: str, first_name: str, last_name: Optional[str] = None, db: Session = Depends(self.get_db)):
            allowed_user = db.query(AllowedUser ).filter(AllowedUser .telegram_id == telegram_id).first()
            if not allowed_user:
                raise HTTPException(status_code=403, detail="Вам не разрешено регистрироваться")

            existing_user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")

            new_user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user

        @self.app.get("/users/{user_id}", response_model=User Schema)
        def read_user(user_id: int, db: Session = Depends(self.get_db)):
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user is None:
                raise HTTPException(status_code=404, detail="User  not found")
            return db_user

        @self.app.post("/send-coin")
        def send_coin(request: UpdatePointsRequest, db: Session = Depends(self.get_db)):
            user = db.query(User).filter(User.telegram_id == request.telegram_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            user.coins += request.coins
            db.commit()
            db.refresh(user)

            return {"message": f"Coin успешно отправлены. Текущее количество coin: {user.coins}"}

        @self.app.post("/api/auth")
        async def auth(data: TelegramAuthData, db: Session = Depends(self.get_db)):
            bot_token = "7217254061:AAEzRMDI0CVS09eAydyRyGMbJjzAZqAGpg4"  # Замените на токен вашего бота if not verify_telegram_data(data, bot_token):
                raise HTTPException(status_code=400, detail="Неверные данные авторизации")

            existing_user = db.query(User).filter(User.telegram_id == data.id).first()
            if existing_user:
                return {"message": "Пользователь уже зарегистрирован"}

            new_user = User(
                telegram_id=data.id,
                username=data.username,
                first_name=data.first_name,
                last_name=data.last_name
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {"message": "Пользователь успешно зарегистрирован", "user": new_user}

        @self.app.post("/api/send-notification")
        async def send_notification(telegram_id: int, message: str):
            bot_token = "7217254061:AAEzRMDI0CVS09eAydyRyGMbJjzAZqAGpg4"
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": telegram_id,
                "text": message
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                if response.status_code != 200:
                    raise HTTPException(status_code=400, detail="Ошибка отправки уведомления")

            return {"message": "Уведомление отправлено"}

        @self.app.get("/products/", response_model=list[ProductSchema])
        def get_all_products(db: Session = Depends(self.get_db)):
            products = db.query(Product).all()
            return products

        @self.app.get("/tasks", response_model=list[TaskSchema])
        def get_tasks(db: Session = Depends(self.get_db)):
            tasks = db.query(Task).all()
            return tasks

        @self.app.get("/products/{product_id}", response_model=ProductSchema)
        def read_product(product_id: int, db: Session = Depends(self.get_db)):
            db_product = db.query(Product).filter(Product.id == product_id).first()
            if db_product is None:
                raise HTTPException(status_code=404, detail="Продукт не найден")
            return db_product

        @self.app.post("/create-task", response_model=TaskSchema)
        def create_task(task: TaskCreate, db: Session = Depends(self.get_db)):
            user = db.query(User).filter(User.id == task.user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            new_task = Task(
                description=task.description,
                points=task.points,
                coins=task.coins,
                deadline=task.deadline,
                user_id=task.user_id
            )

            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            return new_task

        @self.app.post("/products/", response_model=ProductSchema)
        def create_product(product: ProductCreate, db: Session = Depends(self.get_db)):
            new_product = Product(
                name=product.name,
                coins=product.coins
            )

            db.add(new_product)
            db.commit()
            db.refresh(new_product)

            return new_product

# Создаем экземпляр приложения
app_instance = App()
app = app_instance.app