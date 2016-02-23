'''
Created on Feb 23, 2016

@author: root
'''
import pika
from time import sleep

conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

channel = conn.channel()

channel.exchange_declare(exchange="logs", exchange_type="fanout")

rst = channel.queue_declare(exclusive = True)

qname = rst.method.queue

channel.queue_bind(queue=qname, exchange="logs")

print "[*] waiting for logs ..."

def callback(ch, method, properties, body):
    print "log: %s"%body
    sleep(body.count(",")*2)

channel.basic_consume(callback, queue=qname, no_ack=True)

channel.start_consuming()
    
    

