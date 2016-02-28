'''
Created on Feb 28, 2016

@author: root
'''
import pika

if __name__ == "__main__":
    
    items = [
        ["error", "1-errorerrorerrorerror"],
        ["error", "2-errorerrorerrorerror"],
        ["info", "3-infoinfoinfoinfo"],
        ["warning", "4-warningwarningwarningwarning"],
        ["warning", "5-warningwarning"],
        ["error", "6-errorerrorerrorerror"],
        ["info", "7-infoinfoinfoinfoinfo"],
        ["error", "8-errorerrorerrorerror"],
        ["info", "9-infoinfoinfoinfoinfo"],
        ["error", "10-errorerrorerrorerror"],
        ["warning", "11-warningwarningwarning"],
        ["error", "12-errorerrorerrorerror"],
        ["error", "13-errorerrorerrorerror"]
    ]
    
    conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    
    channel = conn.channel()
    
    channel.exchange_declare(exchange="direct_logs", exchange_type="direct")
    
    for item in items:
        channel.basic_publish(
            exchange="direct_logs",
            routing_key=item[0],
            body=item[1]
        )
    
    conn.close()
    
