from pika import ConnectionParameters, BlockingConnection, BasicProperties

connection_params = ConnectionParameters(
    host="localhost",
    port=5672
)

def publish_message(queue_name, message):
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as channel:
            channel.queue_declare(queue=queue_name)

            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message,
                properties=BasicProperties(delivery_mode=2)
            )
            print(f"Message sent to {queue_name}: {message}")