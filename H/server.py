#encoding: utf-8
from pika import BlockingConnection, ConnectionParameters
from pika import BasicProperties

class MyServer(object):
    
    def __init__(self):
        self.conn = BlockingConnection(ConnectionParameters(host="localhost"))
        self.chan = self.conn.channel()
        
    def handler(self, ch, method, props, body):
        print body
        
        ch.queue_declare(queue="response", durable=True)
        ch.basic_publish(
            exchange = "",
            routing_key = "response",
            body = body[::-1],
            properties = BasicProperties(
                delivery_mode = 2       
            )
        )
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
        
    def start(self):
        self.chan.queue_declare(queue="request", durable=True)
        self.chan.basic_consume(consumer_callback=self.handler, queue="request")
        print "开始监听..."
        self.chan.start_consuming()

if __name__ == "__main__":
    ms = MyServer()
    ms.start()
    
    
    
        