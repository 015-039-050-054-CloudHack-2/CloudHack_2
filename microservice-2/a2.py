import pika
import ast 
from pymongo import MongoClient


host = 'rabbitmq-container'
queue="data-queue"

def on_message(ch, method, properties, body):
    message_str = body.decode('UTF-8')
    message=ast.literal_eval(message_str)
   
    # MongoDb connection
    db_host = MongoClient(host='mongodb://root:example@mongo:27017/')
   
    # Inserting data
    db = db_host["rides_db"]
    collection = db["rides_collection"]
    sample_data = {"pickup:":message["pickup"],"destination:":message["destination"],"time":message["time"],"cost":message["cost"],"seats":message["seats"]}
    collection.insert_one(sample_data)
    print('Inserted into the MongoDB database!')

    rec_data = collection.find()
    print("Fetched from Database:")
    for i in rec_data:
        print(i)
        
    
def main():
    print("in database ")
    connection_params = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True)

    print('Subscribed to data' + queue + ', waiting for messages...')
    channel.start_consuming()


if __name__ == '__main__':
    main()