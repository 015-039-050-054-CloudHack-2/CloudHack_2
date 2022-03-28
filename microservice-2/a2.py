from time import time
from traceback import print_tb
import pika
import os
import ast 
import time as t
import json 
from pymongo import MongoClient
host = 'rabbitmq-container'
# queue = os.environ.get('QUEUE_NAME')
queue="data-queue"
def on_message(ch, method, properties, body):
    message_str = body.decode('UTF-8')
    message=ast.literal_eval(message_str)
    print("this is message",message)
    # db_host = MongoClient("")
    db_host = MongoClient(host='mongodb://root:example@mongo:27017/')
    print("works till here",db_host)
    db = db_host["rides_db"]
    collection = db["rides_collection"]
    sample_data = {"Name:":"<YOUR NAME HERE>","SRN":"<YOUR SRN HERE>"}
    collection.insert_one(sample_data)
    print('Inserted into the MongoDB database!')
    rec_data = collection.find()
    for i in rec_data:
        print(i)
        
    # print("Fecthed from MongoDB: ",rec_data)
    # print(message)
    
    
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