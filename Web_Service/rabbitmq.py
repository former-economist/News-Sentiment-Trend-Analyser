# from distutils.command.config import config
# import pika
# import os

# __connection__ = None

# def get_connection():
#     """
#     A function to create a connection to a RabbitMQ message broker server.

#     Returns:
#         Pika: RabbitMQ Server connection.
#     """
#     global __connection__

#     if __connection__ is not None and not __connection__.is_closed:
#         return __connection__

#     configuration = {
#         "RABBITMQ_SERVER": os.environ.get("RABBITMQ_SERVER",""),
#         "RABBITMQ_USER": os.environ.get("RABBITMQ_USER",""),
#         "RABBITMQ_PASSWORD": os.environ.get("RABBITMQ_PASSWORD","")
#     }

#     success = True
#     for value in configuration.values():
#         if len(value) == 0:
#             success = False
#     if not success:
#         __connection__ = None
#         return __connection__

#     credentials = pika.PlainCredentials(username=configuration["RABBITMQ_USER"],
#                                         password=configuration["RABBITMQ_PASSWORD"])
#     parameters = pika.ConnectionParameters(host=configuration["RABBITMQ_SERVER"],
#                                             credentials=credentials)
#     __connection__ = pika.BlockingConnection(parameters)


#     return __connection__

# def get_channel(queue: str):
#     """
#     A function to get a channel and configure a queue.
#     """
#     global __connection__
#     connection = get_connection()
#     if connection is None:
#         return None
#     channel = connection.channel()
#     channel.queue_declare(queue)
#     return channel


# class RabbitMQ:
#     """
#     A class to provide access to RabbitMQ, such that mocking can be used.
#     """
#     def __init__(self, queue: str) -> None:
#         self.queue = queue

#     def publish(self, body: str) -> bool:
#         channel = get_channel(self.queue)
#         if channel is None:
#             logging.error("Could not get a channel to RabbitMQ")
#             return False
#         channel.basic_publish(exchange='', routing_key=self.queue, body=body)
#         return True
