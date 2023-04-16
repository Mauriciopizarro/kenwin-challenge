import pika


class RabbitConnection:

    instance = None

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", heartbeat=999, blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()

    @classmethod
    def get_channel(cls):
        instance = cls.init_connection()
        return instance.channel

    @classmethod
    def get_connection(cls):
        instance = cls.init_connection()
        return instance.connection

    @classmethod
    def init_connection(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    @staticmethod
    def declare_queues(channel, queues):
        for queue in queues:
            channel.queue_declare(queue)
            