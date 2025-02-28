from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from models import User, AllowedUser, Task, Role, Product, TaskStatus
from database import SessionLocal, engine, Base
from schemas import UserSchema, AllowedUserSchema, UpdatePointsRequest, ProductCreate, ProductSchema, LeaderboardUser
import hashlib
import hmac
import httpx
import json
from schemas import TaskCreate, TaskSchema
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import parse_qs
from typing import List

# Создаем таблицы в базе данных (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены (для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модель для запроса на отправку "coin"
class SendCoinRequest(BaseModel):
    telegram_id: int
    coins: int

class UpdateRoleRequest(BaseModel):
    new_role: str

@app.put("/update-role")
def update_user_role(request: UpdateRoleRequest, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = request.new_role
    db.commit()
    return {"message": "Role updated successfully"}

# Модель для данных авторизации Telegram
class TelegramAuthData(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    auth_date: int
    hash: str

# Функция для проверки данных Telegram
def verify_telegram_data(data: TelegramAuthData, bot_token: str) -> bool:
    data_check_string = f"auth_date={data.auth_date}\nfirst_name={data.first_name}\nid={data.id}\nlast_name={data.last_name}\nusername={data.username}"
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return computed_hash == data.hash

# Эндпоинт для начисления баллов
@app.post("/add-points")
def add_points(request: UpdatePointsRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == request.telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.points += request.points
    db.commit()
    db.refresh(user)

    return {"message": f"Баллы успешно добавлены. Текущее количество баллов: {user.points}"}

# Эндпоинт для добавления пользователя в список разрешенных
@app.post("/register", response_model=AllowedUserSchema)
def register_user(telegram_id: int, db: Session = Depends(get_db)):
    existing_user = db.query(AllowedUser).filter(AllowedUser.telegram_id == telegram_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже добавлен")

    new_allowed_user = AllowedUser(telegram_id=telegram_id)
    db.add(new_allowed_user)
    db.commit()
    db.refresh(new_allowed_user)

    return new_allowed_user

# Эндпоинт для регистрации пользователя
@app.post("/start", response_model=UserSchema)
def start_registration(telegram_id: int, username: str, first_name: str, last_name: Optional[str] = None, db: Session = Depends(get_db)):
    allowed_user = db.query(AllowedUser).filter(AllowedUser.telegram_id == telegram_id).first()
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

    return new_user  # Исправлено с new_user

# Эндпоинт для получения лидерборда
@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "name": user.username or "Без имени",
            "level": 1,
            "points": user.points or 0,
            "avatar": None
        }
        for user in users
    ]

# Эндпоинт для получения информации о пользователе по ID
@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Эндпоинт для отправки "coin"
@app.post("/send-coin")
def send_coin(request: SendCoinRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == request.telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.coins += request.coins
    db.commit()
    db.refresh(user)

    return {"message": f"Coin успешно отправлены. Текущее количество coin: {user.coins}"}

# Эндпоинт для авторизации
@app.post("/api/auth")
async def auth(data: TelegramAuthData, db: Session = Depends(get_db)):
    bot_token = "7217254061:AAEzRMDI0CVS09eAydyRyGMbJjzAZqAGpg4"
    if not verify_telegram_data(data, bot_token):
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

# Эндпоинт для отправки уведомлений
@app.post("/api/send-notification")
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

# Эндпоинт для настройки кнопки меню
@app.post("/set-menu-button")
async def set_menu_button(telegram_id: int):
    bot_token = "7217254061:AAEzRMDI0CVS09eAydyRyGMbJjzAZqAGpg4"
    url = f"https://api.telegram.org/bot{bot_token}/setChatMenuButton"
    payload = {
        "chat_id": telegram_id,
        "menu_button": {
            "type": "web_app",
            "text": "Открыть приложение",
            "web_app": {"url": "https://kernew.vercel.app/"}
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Ошибка настройки кнопки")

    return {"message": "Кнопка настроена"}

# Эндпоинт для получения списка всех продуктов
@app.get("/products/", response_model=list[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()  # Исправлено с products = db.query(Product).all()
    return products

# Эндпоинт для получения списка всех задач
@app.get("/tasks", response_model=list[TaskSchema])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@app.get("/products/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return db_product

# Эндпоинт для создания задачи
@app.post("/create-task", response_model=TaskSchema)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == task.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    new_task = Task(
        description=task.description,
        points=task.points,
        coins=task.coins,
        deadline=task.deadline,
        user_id=task.user_id,
        status=task.status
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# Эндпоинт для добавления продукта
@app.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        coins=product.coins
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product  

class PurchaseProductRequest(BaseModel):
    telegram_id: int  # ID пользователя
    product_id: int   # ID продукта

@app.post("/purchase-product")
def purchase_product(request: PurchaseProductRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == request.telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    if user.coins < product.coins:
        raise HTTPException(status_code=400, detail="Недостаточно coins для покупки")

    user.coins -= product.coins
    db.commit()
    db.refresh(user)

    return {"message": f"Продукт '{product.name}' успешно куплен. Остаток coins: {user.coins}"}

# TELEGRAM_BOT_TOKEN = "7317821125:AAE9nlkr4EHMU80W333EIa01OcM_EcKpBQQ"

# def validate_telegram_init_data(init_data: str, bot_token: str) -> dict:
#     parsed_data = parse_qs(init_data)
#     received_hash = parsed_data.get("hash", [""])[0]
#     if not received_hash:
#         raise ValueError("Хэш отсутствует в init_data")

#     data_check_string = "\n".join(
#         f"{key}={parsed_data[key][0]}"
#         for key in sorted(parsed_data.keys())
#         if key != "hash"
#     )

#     secret_key = hmac.new(
#         "WebAppData".encode(),
#         bot_token.encode(),
#         hashlib.sha256
#     ).digest()

#     computed_hash = hmac.new(
#         secret_key,
#         data_check_string.encode(),
#         hashlib.sha256
#     ).hexdigest()

#     if computed_hash != received_hash:
#         raise ValueError("Недействительный хэш: данные были подделаны")

#     user_data = parsed_data.get("user", [""])[0]
#     if not user_data:
#         raise ValueError("Данные пользователя отсутствуют")

#     return json.loads(user_data)

# @app.post("/auth/telegram")
# async def auth_telegram(request: Request, db: Session = Depends(get_db)):
#     # Логируем входящий запрос для отладки
#     print(f"Получен запрос: {request.method} {request.url}")
#     try:
#         data = await request.json()
#         print(f"Тело запроса: {data}")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Неверный формат данных в запросе")

#     init_data = data.get("initData")
#     print(f"Получено initData: {init_data}")

#     if not init_data:
#         raise HTTPException(status_code=400, detail="Данные инициализации отсутствуют")

#     try:
#         user_data = validate_telegram_init_data(init_data, TELEGRAM_BOT_TOKEN)
#         print(f"Валидированные данные пользователя: {user_data}")

#         telegram_id = str(user_data.get("id"))  # Приводим к строке для надежности
#         first_name = user_data.get("first_name", "")
#         last_name = user_data.get("last_name", "")
#         username = user_data.get("username", "")
#         photo_url = user_data.get("photo_url", "https://www.gravatar.com/avatar")

#         # Поиск пользователя в БД
#         user = db.query(User).filter(User.telegram_id == telegram_id).first()

#         if not user:
#             print(f"Создание нового пользователя с telegram_id: {telegram_id}")
#             new_user = User(
#                 telegram_id=telegram_id,
#                 first_name=first_name,
#                 last_name=last_name,
#                 username=username,
#                 points=0,
#                 coins=0,
#                 role=Role.USER
#             )
#             db.add(new_user)
#             db.commit()
#             db.refresh(new_user)
#             user = new_user
#         else:
#             print(f"Найден существующий пользователь: {user.telegram_id}")

#         # Формируем профиль в точности как ожидает фронтенд
#         profile = {
#             "id": user.id,
#             "telegram_id": user.telegram_id,
#             "first_name": user.first_name or "",
#             "last_name": user.last_name or "",
#             "username": user.username or "",
#             "photo_url": photo_url,
#             "points": user.points or 0,
#             "coins": user.coins or 0,
#             "role": user.role.value if user.role else "USER"
#         }

#         # Возвращаем ответ в формате, совместимом с фронтендом
#         return {"profile": profile, "token": init_data}

#     except ValueError as ve:
#         print(f"Ошибка валидации: {str(ve)}")
#         db.rollback()
#         raise HTTPException(status_code=401, detail=f"Ошибка авторизации: {str(ve)}")
#     except Exception as e:
#         print(f"Неизвестная ошибка: {str(e)}")
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

# # Опционально: добавьте обработку GET для отладки (удалите в продакшене)
# @app.get("/auth/telegram")
# async def auth_telegram_get():
#     raise HTTPException(status_code=405, detail="Метод не поддерживается, используйте POST")










# # Ваш Telegram Bot Token от BotFather (вставь свой токен сюда)
# TELEGRAM_BOT_TOKEN = "7317821125:AAE9nlkr4EHMU80W333EIa01OcM_EcKpBQQ"  # Например:

# def validate_telegram_init_data(init_data: str, bot_token: str) -> dict:
#     """
#     Валидация данных инициализации Telegram Mini Apps.
#     Возвращает распарсенные данные пользователя, если валидация успешна.
#     """
#     # Парсим строку init_data в словарь
#     parsed_data = parse_qs(init_data)
    
#     # Извлекаем hash из данных
#     received_hash = parsed_data.get("hash", [""])[0]
#     if not received_hash:
#         raise ValueError("Хэш отсутствует в init_data")

#     # Формируем строку для проверки (все параметры кроме hash, отсортированные по ключу)
#     data_check_string = "\n".join(
#         f"{key}={parsed_data[key][0]}"
#         for key in sorted(parsed_data.keys())
#         if key != "hash"
#     )

#     # Создаем секретный ключ на основе bot_token
#     secret_key = hmac.new(
#         "WebAppData".encode(),
#         bot_token.encode(),
#         hashlib.sha256
#     ).digest()

#     # Вычисляем HMAC-SHA256 от строки проверки
#     computed_hash = hmac.new(
#         secret_key,
#         data_check_string.encode(),
#         hashlib.sha256
#     ).hexdigest()

#     # Сравниваем вычисленный hash с полученным
#     if computed_hash != received_hash:
#         raise ValueError("Недействительный хэш: данные были подделаны")

#     # Если валидация прошла, возвращаем распарсенные данные
#     user_data = parsed_data.get("user", [""])[0]
#     if not user_data:
#         raise ValueError("Данные пользователя отсутствуют")

#     import json
#     return json.loads(user_data)

# @app.post("/auth/telegram")
# async def auth_telegram(request: Request):
#     data = await request.json()
#     init_data = data.get("initData")

#     if not init_data:
#         raise HTTPException(status_code=400, detail="Данные инициализации отсутствуют")

#     try:
#         # Валидация и парсинг данных от Telegram
#         user = validate_telegram_init_data(init_data, TELEGRAM_BOT_TOKEN)
        
#         # Формируем данные профиля
#         profile = {
#             "id": user.get("id"),
#             "first_name": user.get("first_name"),
#             "last_name": user.get("last_name"),
#             "username": user.get("username"),
#             "photo_url": user.get("photo_url", "https://www.gravatar.com/avatar")
#         }
        
#         return {"profile": profile, "token": init_data}  # Возвращаем профиль и исходный initData как токен
        
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Ошибка авторизации: {str(e)}")





# Ваш Telegram Bot Token от BotFather
TELEGRAM_BOT_TOKEN = "7317821125:AAE9nlkr4EHMU80W333EIa01OcM_EcKpBQQ"


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_telegram_init_data(init_data: str, bot_token: str) -> dict:
    """
    Валидация данных инициализации Telegram Mini Apps.
    Возвращает распарсенные данные пользователя, если валидация успешна.
    """
    parsed_data = parse_qs(init_data)
    received_hash = parsed_data.get("hash", [""])[0]
    if not received_hash:
        raise ValueError("Хэш отсутствует в init_data")

    data_check_string = "\n".join(
        f"{key}={parsed_data[key][0]}"
        for key in sorted(parsed_data.keys())
        if key != "hash"
    )

    secret_key = hmac.new(
        "WebAppData".encode(),
        bot_token.encode(),
        hashlib.sha256
    ).digest()

    computed_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if computed_hash != received_hash:
        raise ValueError("Недействительный хэш: данные были подделаны")

    user_data = parsed_data.get("user", [""])[0]
    if not user_data:
        raise ValueError("Данные пользователя отсутствуют")

    return json.loads(user_data)

@app.post("/auth/telegram")
async def auth_telegram(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    init_data = data.get("initData")

    if not init_data:
        raise HTTPException(status_code=400, detail="Данные инициализации отсутствуют")

    try:
        # Валидация и парсинг данных от Telegram
        user_data = validate_telegram_init_data(init_data, TELEGRAM_BOT_TOKEN)
        
        # Извлекаем данные пользователя
        telegram_id = user_data.get("id")
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        username = user_data.get("username")
        photo_url = user_data.get("photo_url", "https://www.gravatar.com/avatar")

        # Проверяем, существует ли пользователь в базе
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            # Если пользователя нет, создаем нового
            new_user = User(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                points=10,  # Начальные значения
                coins=150,
                role=Role.USER
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user

        # Формируем данные профиля для ответа
        profile = {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "photo_url": photo_url,
            "points": user.points,
            "coins": user.coins,
            "role": user.role.value  # Используем .value для строкового представления роли
        }
        
        return {"profile": profile, "token": init_data}  # Возвращаем профиль и исходный initData как токен
        
    except Exception as e:
        db.rollback()  # Откатываем изменения в случае ошибки
        raise HTTPException(status_code=401, detail=f"Ошибка авторизации: {str(e)}")

class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus

@app.put("/tasks/{task_id}/status")
def update_task_status(task_id: int, request: UpdateTaskStatusRequest, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    task.status = request.status
    db.commit()
    db.refresh(task)
    
    return {"message": "Статус задачи успешно обновлен", "status": task.status}