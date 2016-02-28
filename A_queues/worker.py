#encoding: utf-8
'''
Created on Feb 22, 2016

@author: root
'''
#!/usr/bin/env python  
import pika  
import time
  
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  
channel = connection.channel()  
  
channel.queue_declare(queue='hello', durable=True)  
  
print ' [*] Waiting for messages. To exit press CTRL+C'  
  
def callback(ch, method, properties, body):  
    print " [x] Received %r" % (body,)
    
    time.sleep(body.count(",")*0.003)
    
    print "[x] Done."
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

#channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    callback,
    queue='hello'
    #no_ack=True, 需不需要ack在从队列里取消息的时候指定，是否需要还是取绝于是否相信callback
)  
  
channel.start_consuming()  