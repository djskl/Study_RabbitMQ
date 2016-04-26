#encoding: utf-8
'''
Created on Mar 4, 2016

@author: root
'''
import pika, uuid
import threading
import sys
from time import sleep

class FibClient(object):
    
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.conn.channel()
        
        rst = self.channel.queue_declare(queue="hello", durable=True)
        self.callback_queue = rst.method.queue
        
        self.channel.basic_consume(self.on_response, queue=self.callback_queue, no_ack=True)
    
    def on_response(self, ch, method, props, body):
        print self.coorid, props.correlation_id, body
        self.response = body
        
    def call(self, n):
        self.response = None
        self.coorid = str(n)
        
        self.channel.basic_publish(exchange="",
                                   routing_key="rpc_queue",
                                   body=str(n),
                                   properties=pika.BasicProperties(
                                       reply_to = self.callback_queue,
                                       correlation_id = self.coorid
                                   ))
        print "%d: sent"%n
        
        while self.response is None:
            self.conn.process_data_events(None)
        
if __name__ == "__main__":   
    
    num = int(sys.argv[1])
    
    fc = FibClient()
    
    fc.call(num)
    
        
        
        