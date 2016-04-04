'''
Created on Apr 3, 2016

@author: root
'''
from pika import BlockingConnection, ConnectionParameters
from constants import RBT_HOST
import threading

def create_basic_channel():
    conn = BlockingConnection(ConnectionParameters(host=RBT_HOST))
    chan = conn.channel()
    
    return conn, chan

def async_call(func, *args, **kwargs):
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    t.start()
    
