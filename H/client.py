'''
Created on Apr 18, 2016

@author: root
'''
from pika import BlockingConnection, ConnectionParameters
from pika import BasicProperties


class MyClient(object):
    
    def __init__(self):
        self.conn = BlockingConnection(ConnectionParameters(host="localhost"))
        self.chan = self.conn.channel()
    
    def handler(self, ch, method, props, body):
        print body
        ch.basic_ack(delivery_tag = method.delivery_tag)
        ch.stop_consuming()
        
    def reverse(self, s):
        self.chan.queue_declare(queue="request", durable=True)
        self.chan.basic_publish(
            exchange="",
            routing_key="request",
            body=s,
            properties = BasicProperties(
                delivery_mode = 2
            )
        )
        
        self.chan.queue_declare(queue="response", durable=True)
        self.chan.basic_consume(
            consumer_callback = self.handler,
            queue = "response"
        )
        self.chan.start_consuming()

if __name__ == "__main__":
    mc = MyClient()
    msgs = ["hello", "world", "zxh", "1988"]
    for msg in msgs:
        mc.reverse(msg)
    
    
    
        