'''
Created on Apr 3, 2016

@author: root
'''
from pika import BlockingConnection, ConnectionParameters
from constants import RBT_HOST

def create_basic_channel():
    conn = BlockingConnection(ConnectionParameters(host=RBT_HOST))
    chan = conn.channel()
    
    return conn, chan
    
