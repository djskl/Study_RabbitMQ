#encoding: utf-8
'''
Created on Apr 3, 2016

@author: root
'''
import json
from datetime import datetime, timedelta

ALL_TASKS = {}

class TaskInfo(object):
    
    def __init__(self, **kwargs):
        self.taskid = kwargs.get("taskid")
        self.progress = kwargs.get("progress")
        self.stime = kwargs.get("stime")
        self.etime = kwargs.get("etime")
        self.error_code = kwargs.get("error_code")
        self.error_info = kwargs.get("error_info")
        self.result = kwargs.get("result")
    
    def __str__(self):
        return json.dumps({
            "taskid": self.taskid,
            "progress": self.progress,
            "stime": self.stime.strftime("%Y-%m-%d %H:%M:%S") if self.stime else None, 
            "etime": self.etime.strftime("%Y-%m-%d %H:%M:%S") if self.etime else None, 
            "error_code": self.error_code, 
            "error_info": self.error_info,
            "result": self.result
        })

class TaskMeta(type):
    def __new__(self, *args, **kwargs):
        clz = super(TaskMeta, self).__new__(self, *args, **kwargs)
        ALL_TASKS[clz.task_type] = clz
        return clz

class BaseTask(object):
    
    report_taskinfo = None
    
    def set_report_func(self, func):
        self.report_taskinfo = func    
        
    def do(self, taskid, **kwargs):
        
        taskInfo = TaskInfo(taskid = taskid, stime = datetime.now())
        
        self.report_taskinfo(taskInfo)
        
        print json.dumps(kwargs)
        
        taskInfo.etime = datetime.now() + timedelta(hours=1)
        taskInfo.result = "hello, world"
        self.report_taskinfo(taskInfo)
        
        
class A(BaseTask):
    __metaclass__ = TaskMeta
    task_type = "abc"
    

class B(BaseTask):
    __metaclass__ = TaskMeta
    task_type = "def"
    
    