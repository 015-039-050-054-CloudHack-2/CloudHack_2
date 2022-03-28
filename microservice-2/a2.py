from time import time
import pika
import os
import ast 
import time as t
import json 
host = 'rabbitmq-container'
queue = os.environ.get('QUEUE_NAME')
def on_message(ch, method, properties, body):
    message = body.decode('UTF-8')
    # message=ast.literal_eval(message_str)
    # key = (message["name"],message["IP"])
    # value=(message["consumer_id"],message["request_IP"])
    # data_dict={}
    # data_dict[str(key)]=str(value)
    print(message)
    
    
def main():
    connection_params = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True)

    print('Subscribed to data' + queue + ', waiting for messages...')
    channel.start_consuming()
if __name__ == '__main__':
    main()