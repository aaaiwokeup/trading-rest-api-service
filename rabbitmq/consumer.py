from pika import ConnectionParameters, BlockingConnection

connection_params = ConnectionParameters(
    host="localhost",
    port=5672
)

def process_message(ch, method, properties, body):
    print(f"Message received: {body.decode()}")


def get_messages(queue_name):
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as channel:
            channel.queue_declare(queue=queue_name)

            channel.basic_consume(
                queue=queue_name,
                on_message_callback=process_message
            )
            print("Wait for messages")
            channel.start_consuming()


if __name__ == "__main__":
    get_messages("strategy_queue")