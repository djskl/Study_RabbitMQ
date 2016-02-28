'''
Created on Feb 28, 2016

@author: root
'''
import pika
from time import sleep

conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

channel = conn.channel()

channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

rst = channel.queue_declare(exclusive = True)
queue_name = rst.method.queue

channel.queue_bind(queue=queue_name, exchange="direct_logs", routing_key="error")

def _callback(ch, method, properties, body):
    sleep(1)
    with open("log.error", "a") as writer:
        writer.write("[x] %s: %s\n"%(method.routing_key, body))
    
channel.basic_consume(_callback, queue=queue_name, no_ack=True)

channel.start_consuming()
    

