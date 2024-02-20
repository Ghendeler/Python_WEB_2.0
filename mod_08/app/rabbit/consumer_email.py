import json
import pika
import sys

import connect
from models import Customer


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='by_email')

    def callback(ch, method, properties, body):
        body_decoded = body.decode('utf8')
        json_recivede = json.loads(body_decoded)
        customer = Customer.objects(id=json_recivede['id']).first()
        Customer.objects(id=json_recivede['id']).update(sended=True)
        print(f" [x] Sended email to {customer.fullname} - {customer.email}")

    channel.basic_consume(
        queue='by_email',
        on_message_callback=callback,
        auto_ack=True
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
