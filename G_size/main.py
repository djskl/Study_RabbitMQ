'''
Created on Apr 5, 2016

@author: root
'''
from pika import BlockingConnection, ConnectionParameters
from pika import BasicProperties
from time import sleep

conn = BlockingConnection(ConnectionParameters(host="127.0.0.1"))
chan = conn.channel()

msg = None
with open("data.txt") as reader:
    msg = reader.read()

for _ in range(500):
    chan.basic_publish(
        exchange="",
        routing_key="response",
        body=msg,
        properties=BasicProperties(delivery_mode=2)
    )