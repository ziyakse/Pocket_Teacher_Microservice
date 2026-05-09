# auth_service/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika, json, jwt
from datetime import datetime, timedelta
import os
from passlib.context import CryptContext
from prometheus_fastapi_instrumentator import Instrumentator

# Veritabanını diğer dosyadan içeri aktarıyoruz
from mock_db import MOCK_USERS_DB

app = FastAPI(title="Pocket Teacher Auth Service")



Instrumentator().instrument(app).expose(app)


# GÜVENLİK 1: Gizli anahtarı koda yazmıyoruz, çevresel değişkenden alıyoruz
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_gizli_anahtar_degistirilecek")

# GÜVENLİK 2: Şifreleri çözmek için Bcrypt ayarı
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

# --- İZLENEBİLİRLİK (HAFTA 4) ---
@app.get("/health")
def read_health():
    """Kubernetes veya API Gateway'in servisin ayakta olup olmadığını anlaması için Health Check"""
    return {"status": "ok", "service": "auth-service"}
# --------------------------------

@app.post("/api/auth/login")
def login(user: LoginData):
    # 1. Kullanıcının gönderdiği email mock veritabanımızda (mock_db) var mı kontrol et
    db_user = MOCK_USERS_DB.get(user.email)
    
    # 2. Kullanıcı varsa ve şifresi EŞLEŞİYORSA (Bcrypt ile hash doğrulaması yapıyoruz)
    if db_user and pwd_context.verify(user.password, db_user["password"]):
        
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

# --- PROMETHEUS METRİKLERİ ---
@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)