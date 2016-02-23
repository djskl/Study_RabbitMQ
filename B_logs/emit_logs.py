'''
Created on Feb 23, 2016

@author: root
'''
import pika
class Logs(object):
    
    def __init__(self, host="localhost"):
        self.host = host
    
    def __call__(self, func):
        
        def _wraper(*args, **kwargs):
            
            try:
                kwargs["conn"] = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            
                func(*args, **kwargs)
            finally:
                kwargs["conn"].close()
                
        return _wraper
@Logs()           
def send(*args, **kwargs):
    
    conn = kwargs["conn"]
    
    channel = conn.channel()
    
    channel.exchange_declare(exchange="logs", exchange_type="fanout")
    
    msg = ",".join(args) or "info: empty log"
    
    channel.basic_publish(exchange="logs", routing_key="", body=msg)
    
    print "[x] sent: %s"%msg

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
    
    
    
    
    
    
    
    
            
            
            
            
        
    
