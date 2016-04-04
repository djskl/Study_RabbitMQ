#encoding: utf-8
'''
Created on Apr 2, 2016

@author: root
'''
import json
from pika import BasicProperties
from utils import create_basic_channel, async_call
from constants import TASK_EXH, TASK_QUE, STAT_QUE

class TaskClient(object):
    
    def __init__(self):
        
        self.conn, self.chan = create_basic_channel()
    
        self.chan.exchange_declare(exchange=TASK_EXH, exchange_type="topic", durable=True)
        self.chan.queue_declare(queue=TASK_QUE, durable=True)
    
        self.chan.queue_declare(queue=STAT_QUE, durable=True)
        self.chan.basic_consume(self.on_response, queue=STAT_QUE)
        async_call(self.chan.start_consuming)
        
    def on_response(self, ch, method, props, body):
        print props.correlation_id
        print body
        
        taskinfo = json.loads(body)
        
        if taskinfo["result"]:
            ch.stop_consuming()
            
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    
    def submit(self, task_id, task_type, task_params):
        
        self.chan.queue_bind(queue=TASK_QUE, exchange=TASK_EXH, routing_key=task_type)
        
        self.chan.basic_publish(exchange=TASK_EXH,
                           routing_key=task_type,
                           body=json.dumps({
                                "taskid": task_id,
                                "params": task_params
                           }),
                           properties=BasicProperties(
                                delivery_mode = 2,
                                correlation_id = task_id
                           ))
        
        return True
        
if __name__ == "__main__":
    
    tc = TaskClient()
    
    print tc.submit("task_0001", "abc", {"one": 1, "two": 2})


