#encoding: utf-8
'''
Created on Mar 4, 2016

@author: root
'''
import pika
from time import sleep

class RpcServer(object):
    
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue="rpc_queue")
        
    def fibs(self, n):
        n1, n2 = 0, 1
        while True:
            yield n1
            if n1 > n:
                break
            n1, n2 = n2, n1+n2
    
    def triple(self, n):
        return n*3
    
    def on_request(self, ch, method, props, body):
        n = int(body)
        rst = self.triple(n)
        print "fibs(%s)"%n
        sleep(n)
        ch.basic_publish(
            exchange = "",
            routing_key = props.reply_to,
            properties = pika.BasicProperties(
                correlation_id = props.correlation_id
            ),
            body = str(rst)
        )
        print "%d: over"%n
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    def start_listen(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            self.on_request,
            queue="rpc_queue"
        )
        self.channel.start_consuming()

if __name__ == "__main__":
    rs = RpcServer()
    print "开始监听。。。"
    rs.start_listen()
    