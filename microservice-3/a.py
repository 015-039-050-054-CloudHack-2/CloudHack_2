import socket
import requests
import pika
import os
import ast 
import time as t
import json
import random
import socket

host = 'rabbitmq-container'
queue = os.environ.get('QUEUE_NAME')

consumer_arrays={}
consumer_ip=socket.gethostbyname(socket.gethostname())
server_ip=socket.gethostbyname('cc-producer')
print("----------------c",consumer_ip)
print("----------------s",server_ip)

def register_as_consumer():
    if((os.environ.get('CONSUMER_NAME'),consumer_ip) not in consumer_arrays.keys()):
        url="http://cc-producer:3000/new_ride_matching_consumer"
        b={
            "consumer_id":11,
            "consumer_ip":consumer_ip,
            "consumer_name":os.environ.get('CONSUMER_NAME'),
            "request_ip": server_ip
        }
        s1 = requests.post(
            url, 
            headers={"content-type":"application/json"},
            data=json.dumps(b))
        key=(os.environ.get('CONSUMER_NAME'),consumer_ip)
        value=[11,"172.25.0.101"]
        consumer_arrays[key]=value
        print(consumer_arrays)
        print("s1",s1.content)
    return None


def on_message(ch, method, properties, body):
    message = body.decode('UTF-8')
    message_str = body.decode('UTF-8')
    message=ast.literal_eval(message_str)
    time = message["time"]
    print("Current consumer sleeps for ",time," seconds!")
    t.sleep(time)
    task_id=random.randint(1,100)
    print("task_id:",task_id,"Ride Details:", message)
    
def main():
    print("env ",os.environ)
    print("socket " ,socket.gethostbyname(socket.gethostname()))
    print("registering will begin")
    register_as_consumer()
    print("registering has ended")

    connection_params = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue)
    
    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True)

    print('Subscribed to ' + queue + ', waiting for messages...')
    channel.start_consuming()
   



if __name__ == '__main__':
    main()