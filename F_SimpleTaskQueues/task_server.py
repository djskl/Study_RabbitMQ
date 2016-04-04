#encoding: utf-8
'''
Created on Apr 3, 2016

@author: root
'''
import json
from pika import BasicProperties
from tasks import ALL_TASKS, TaskInfo
from utils import create_basic_channel
from constants import TTYPES, TASK_EXH, TASK_QUE, STAT_EXH, STAT_QUE

'''
负责任务的接受与状态汇报
'''
class TaskServer(object):
    
    def __init__(self):
        self.chan = create_basic_channel()[1]  
        
        #任务接受exchange&queue
        self.chan.exchange_declare(exchange=TASK_EXH, exchange_type="topic", durable=True)
        self.chan.queue_declare(queue=TASK_QUE, durable=True)
        for tt in TTYPES:
            self.chan.queue_bind(queue=TASK_QUE, exchange=TASK_EXH, routing_key=tt)
        
        #状态报告exchange&queue
        self.chan.queue_declare(queue=STAT_QUE, durable=True)
    
    def report(self, stat):
        if type(stat) <> TaskInfo:
            return False
        
        self.chan.basic_publish(
            exchange = "",  
            routing_key = STAT_QUE,
            properties = BasicProperties(
                correlation_id = stat.taskid
            ),  
            body = str(stat)
        )
    
    def _cb(self, ch, method, props, body):
        task_type = method.routing_key
        args = json.loads(body)
        
        Task = ALL_TASKS.get(task_type)
        
        if not Task:
            ch.basic_ack(delivery_tag = method.delivery_tag)
            return
        
        task = Task()
        task.set_report_func(self.report)
        task.do(args["taskid"], **args["params"])
        
        ch.basic_ack(delivery_tag = method.delivery_tag)
    
    def start(self):
        print "开始监听。。。"
        self.chan.basic_consume(self._cb, queue=TASK_QUE)
        self.chan.start_consuming()
        
if __name__ == "__main__":
    ts = TaskServer()
    ts.start()
    
        
