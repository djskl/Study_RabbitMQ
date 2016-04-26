'''
Created on Apr 5, 2016

@author: root
'''
from pika import BlockingConnection, ConnectionParameters
from pika import BasicProperties

conn = BlockingConnection(ConnectionParameters(host="127.0.0.1"))
chan = conn.channel()

chan.queue_declare(queue="request", arguments={
    "x-max-length": 10                                          
})

msg = "hello"
for _ in range(15):
    chan.basic_publish(
        exchange="",
        routing_key="request",
        body=msg,
        properties=BasicProperties(delivery_mode=2)
    )