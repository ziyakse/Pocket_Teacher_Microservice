# 1. Python imajını kullan
FROM python:3.10-slim

# 2. Çalışma dizinini ayarla
WORKDIR /app

# 3. Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Tüm proje dosyalarını kopyala
# Python'a mevcut dizini paket olarak görmesini söylüyoruz
ENV PYTHONPATH=/app
COPY . .

# 5. Flask uygulamasını çalıştır (Port 5000)
# Not: Uygulamanın giriş noktası app/finance.py olduğu için bunu çalıştırıyoruz
CMD ["python", "app/finance.py"]