import pika
from os import environ

hostname = environ.get('rabbit_host') or 'localhost'
port = environ.get('rabbit_port') or 5672
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600,
))
channel = connection.channel()
exchangename= "email_topic"
exchangetype= "topic"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)

############   Email queue   #############
queue_name = 'email'
channel.queue_declare(queue=queue_name, durable=True)
routing_key = '#.order'

channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key=routing_key)

    

"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'topic' exchange to be used by the microservices in the solution.
"""
def check_setup():
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True) ###


def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
