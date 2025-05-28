import json
import pika
from bson import ObjectId
from faker import Faker
from contact import Contact
import connect

fake = Faker()

def produce_contacts(n=10):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue', durable=True)

    for _ in range(n):
        fullname = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        notes = fake.sentence()

        # Создаём контакт в БД
        contact = Contact(fullname=fullname, email=email, phone=phone, notes=notes)
        contact.save()

        message = json.dumps({"contact_id": str(contact.id)})
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        print(f"Sent to queue: {message}")

    connection.close()

if __name__ == "__main__":
    produce_contacts(10)
