# auth_service/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika, json, jwt
from datetime import datetime, timedelta

# Veritabanını diğer dosyadan içeri aktarıyoruz
from mock_db import MOCK_USERS_DB

app = FastAPI(title="Pocket Teacher Auth Service")
SECRET_KEY = "*************"

class LoginData(BaseModel):
    email: str
    password: str

def publish_event(event_type: str, data: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='notifications')
        event = {"type": event_type, "data": data}
        channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(event))
        connection.close()
    except Exception as e:
        print("RabbitMQ Hatası:", e)

@app.post("/api/auth/login")
def login(user: LoginData):
    # 1. Kullanıcının gönderdiği email sahte veritabanımızda (mock_db) var mı kontrol et
    db_user = MOCK_USERS_DB.get(user.email)
    
    # 2. Kullanıcı varsa ve şifresi eşleşiyorsa token üret
    if db_user and db_user["password"] == user.password:
        
        token = jwt.encode(
            {
                "sub": user.email, 
                "name": db_user["name"],
                "role": db_user["role"],
                "exp": datetime.utcnow() + timedelta(hours=1)
            }, 
            SECRET_KEY, algorithm="HS256"
        )
        
        # 3. Asenkron iletişim: Login bilgisini RabbitMQ'ya gönder
        publish_event("USER_LOGIN", {"email": user.email, "name": db_user["name"], "time": str(datetime.utcnow())})
        
        return {"access_token": token, "token_type": "bearer"}
    
    # E-posta yoksa veya şifre yanlışsa hata dön
    raise HTTPException(status_code=401, detail="Geçersiz kimlik bilgileri")
