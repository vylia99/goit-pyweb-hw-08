import json
import pika
from contact import Contact
import connect

def send_email_stub(contact):
    # заглушка для отправки письма
    print(f"Відправка листа на {contact.email} для {contact.fullname}")

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data.get("contact_id")
    if not contact_id:
        print("Не отримано contact_id")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    contact = Contact.objects(id=contact_id).first()
    if not contact:
        print(f"Контакт з id {contact_id} не знайдено.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    if contact.sent:
        print(f"Лист вже відправлено контакту {contact.email}")
    else:
        send_email_stub(contact)
        # Встановлюємо поле sent = True
        contact.sent = True
        contact.save()
        print(f"Статус 'sent' оновлено для {contact.email}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    print('Очікування повідомлень. Для виходу натисніть CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    consume()
