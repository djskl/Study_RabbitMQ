'''
Created on Mar 1, 2016

@author: root
'''
import pika

class Sender(object):
    
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.conn.channel()
        
        self.channel.exchange_declare(exchange="topic_exchange", exchange_type="topic")
        
    def publish(self, rkey, msg):
        self.channel.publish(exchange="topic_exchange", routing_key=rkey, body=msg)
        print "%s: %s"%(rkey, msg)
        
        
    def close(self):
        self.conn.close()    
    

if __name__ == "__main__":
    s = Sender()
    
    items = [
        ["cron.error", "cron.error.cron.error.cron.error.cron.error"],
        ["auth.info", "1"],
        ["auth.error", "auth.error.auth.error.auth.error"],
        ["kern.error", "kern.error.kern.error"],
        ["kern.info", "kern.info.kern.info.kern.info"],
        ["cron.error", "cron.error.cron.error.cron.error.cron.error"],
        ["cron.info", "cron.info"],
        ["cron.error", "cron.error.cron.error.cron.error.cron.error"],
        ["auth.info", "2"],
        ["cron.error", "cron.error.cron.error.cron.error.cron.error"],
        ["auth.info", "3"]
    ]
    
    s = Sender()
    
    for item in items:
        s.publish(item[0], item[1])
    
    
    
    