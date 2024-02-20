import json
import pika

import connect
from models import Customer


def get_send_list():
    result = Customer.objects().limit(30)
    return result


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello_world')
    channel.queue_declare(queue='by_email')
    channel.queue_declare(queue='by_sms')

    send_list = get_send_list()
    for s in send_list:
        body = {
            "id": str(s.id),
            "fullname": s.fullname,
            "email": s.email,
            "phone": s.phone
        }
        if s.notification_method == 'email':
            channel.basic_publish(
                exchange='',
                routing_key='by_email',
                body=json.dumps(body)
            )
        elif s.notification_method == 'sms':
            channel.basic_publish(
                exchange='',
                routing_key='by_sms',
                body=json.dumps(body)
            )

    print(" [x] Sent 'Hello World!'")
    connection.close()


if __name__ == '__main__':
    main()
