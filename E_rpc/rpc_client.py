#encoding: utf-8
'''
Created on Mar 4, 2016

@author: root
'''
import pika, uuid

class FibClient(object):
    
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.conn.channel()
        
        rst = self.channel.queue_declare(exclusive=True)
        self.callback_queue = rst.method.queue
        
        self.channel.basic_consume(self.on_response, queue=self.callback_queue, no_ack=True)
    
    def on_response(self, ch, method, props, body):
        if self.coorid == props.correlation_id:
            self.response = body
            
    def call(self, n):
        self.response = None
        self.coorid = str(uuid.uuid4())
        
        self.channel.basic_publish(exchange="",
                                   routing_key="rpc_queue",
                                   body=str(n),
                                   properties=pika.BasicProperties(
                                       reply_to = self.callback_queue,
                                       correlation_id = self.coorid
                                   ))
        
        while self.response is None:
            self.conn.process_data_events()
            
        return int(self.response)
    
if __name__ == "__main__":
    fc = FibClient()
    
    print fc.call(6)
        
        
        
        
        
        