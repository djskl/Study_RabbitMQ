'''
Created on Mar 1, 2016

@author: root
'''
import pika
import threading

class Logger(object):
    
    def __init__(self, name, rkeys):
        self._rkeys = rkeys or "#"
        self._name = name
    
    def _callback(self, ch, method, properties, body):
        print "[ %s ]: %s %s"%(self._name, method.routing_key, body)
    
    def startReceive(self):
        conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        channel = conn.channel()
        
        channel.exchange_declare(exchange="topic_exchange", exchange_type="topic")
        
        rst = channel.queue_declare(exclusive=True)
        queue_name = rst.method.queue
        
        for rk in self._rkeys:
            channel.queue_bind(queue=queue_name, exchange="topic_exchange", routing_key=rk)
        
        channel.basic_consume(self._callback, queue=queue_name, no_ack=True)
        
        print ' [%s] Waiting for logs. To exit press CTRL+C'%self._name        
        channel.start_consuming()
        
if __name__ == "__main__":
    
    log1 = Logger("log1", ["#.error"])
    
    log2 = Logger("log2", ["cron.*"])
    
    log3 = Logger("log3", ["auth.info"])
    
    t1 = threading.Thread(target=log1.startReceive)
    t1.start()
    
    t2 = threading.Thread(target=log2.startReceive)
    t2.start()
    
    t3 = threading.Thread(target=log3.startReceive)
    t3.start()
    
            
