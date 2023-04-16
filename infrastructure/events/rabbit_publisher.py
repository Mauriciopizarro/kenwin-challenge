import json
from domain.interfaces.publisher import Publisher
from infrastructure.events.rabbit_connection import RabbitConnection


class RabbitPublisher(Publisher):

    def send_message(self, message: dict, topic: str):
        """Method to publish message to RabbitMQ"""
        publish_queue_name = topic
        channel = RabbitConnection.get_channel()

        channel.basic_publish(
            exchange='',
            routing_key=publish_queue_name,
            body=json.dumps(message)
        )
