from email import message
from email.quoprimime import body_check
from urllib import response
from wsgiref import headers
import pika
import os
import socket
import requests
from time import time
import pika
import os
import ast 
import time as t
import json
host = 'rabbitmq-container'
queue = os.environ.get('QUEUE_NAME')
def register_as_consumer():
    url="http://cc-producer:3000/new_ride_matching_consumer"
    headers={'User-Agent':'Mozilla/5.0'}
    b={
        "consumer_id":"a",
        "consumer_ip":"a",
        "onsumer_name":"a",
        "request_ip":"s"
    }
    s1 = requests.post(
    url, 
    headers={"content-type":"application/json"},
    data=json.dumps(b))
    # t=json.dumps(b)
    # print(t)
    # response=requests.post(url,params=b)
    # r=requests.post(url,params=t)
    # print(response.content)
    print(s1.content)
    return None
def on_message(ch, method, properties, body):
    message = body.decode('UTF-8')
    #print(message.content)
    message_str = body.decode('UTF-8')
    message=ast.literal_eval(message_str)
    time = message["time"]
    print(message)
    t.sleep(time)
    print(message)
    
def main():
    connection_params = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True)

    print('Subscribed to ' + queue + ', waiting for messages...')
    channel.start_consuming()
    print(os.environ)
    print(socket.gethostbyname(socket.gethostname()))
    # print("registering will begin")
    register_as_consumer()
    # print("registering has ended")




if __name__ == '__main__':
    main()