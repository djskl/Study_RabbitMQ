'''
Created on Feb 22, 2016

@author: root
'''
#!/usr/bin/env python  
import pika

class RbTask(object):
    
    def __init__(self, host="localhost"):
        self.host = host
        
    def __call__(self, func):
        def _wraper(*args, **kwargs):
            try:
                _conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
                print "connected"   
                kwargs["conn"] = _conn
                func(*args, **kwargs)
            finally:
                _conn.close()
                print "close connection"
        
        return _wraper
    

@RbTask()
def send(*args, **kwargs):
    conn = kwargs["conn"]
    channel = conn.channel()
    channel.queue_declare(queue='hello', durable=True)
    msg = ",".join(args) or "hello,world"
    
    channel.basic_publish(exchange='',  
                      routing_key='hello',  
                      body=msg,
                      properties=pika.BasicProperties(
                        delivery_mode = 2,
                      ))
    
    print "send %s" % msg
    
if __name__ == "__main__":
    
    msgs = [
        ["1","2"],
        ["2","2","2"],
        ["3","3","3","3"],
        ["4","4","4","4","4"],
        ["5","5","5","5","5","5"],
    ]
    
    for msg in msgs:
        send(*msg)
    
    
    
    