#encoding: utf-8
'''
Created on Apr 2, 2016

@author: root
'''
import json
from pika import BasicProperties
from utils import create_basic_channel
from constants import TASK_EXH, TASK_QUE, STAT_QUE

class TaskClient(object):
    
    def __init__(self):
        
        self.conn, self.chan = create_basic_channel()
    
        self.chan.exchange_declare(exchange=TASK_EXH, exchange_type="topic", durable=True)
        self.chan.queue_declare(queue=TASK_QUE, durable=True)
    
        self.chan.queue_declare(queue=STAT_QUE, durable=True)
        
        
    def submit(self, task_id, task_type, task_params): 
        
        self.result = None
        def on_response(ch, method, props, body):
            if task_id == props.correlation_id:
                self.result = json.loads(body)
        
        self.chan.queue_bind(queue=TASK_QUE, exchange=TASK_EXH, routing_key=task_type)
        
        self.chan.basic_publish(exchange=TASK_EXH,
                           routing_key=task_type,
                           body=json.dumps({
                                "taskid": task_id,
                                "params": task_params
                           }),
                           properties=BasicProperties(
                                delivery_mode = 2,
                                reply_to = STAT_QUE,
                                correlation_id = task_id
                           ))
        
        self.chan.basic_consume(on_response, no_ack=True, queue=STAT_QUE)
        
        while self.result is None:
            print "等待结果。。。"
            self.conn.process_data_events()
         
        return self.result 
        
if __name__ == "__main__":
    
    tc = TaskClient()
    
    print tc.submit("task_0001", "abc", {"one": 1, "two": 2})


