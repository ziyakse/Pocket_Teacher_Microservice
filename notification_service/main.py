import pika, json, time

def callback(ch, method, properties, body):
    event = json.loads(body)
    event_type = event.get("type")
    data = event.get("data", {})
    
    if event_type == "USER_LOGIN":
        print(f"✅ GİRİŞ YAPILDI: {data.get('email')} sisteme giriş yaptı.")
    elif event_type == "SOCIAL_IMPACT":
        print(f"🌟 SOSYAL ETKİ: {data.get('purchaser')} adlı kullanıcı, {data.get('supported')} adlı öğrenciye Premium destek sağladı! Teşekkür maili gönderiliyor...")

def start():
    time.sleep(15) # RabbitMQ'nun hazır olmasını bekle
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    
    print('🔔 Notification Service dinliyor...')
    channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    start()