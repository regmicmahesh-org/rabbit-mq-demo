#importing pika
import sys
import pika

#saving credentials to access the rabbitmq server
credentials = pika.PlainCredentials(username='guest', password='guest')


#establishing connection to rabbitmq server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.6.0.7', credentials=credentials))

#establishing a channel to communicate with exchange
channel = connection.channel()


#callback function which will be called on every new message on the queue.
def callback(ch, method, properties , body):
    body_str = body.decode('utf-8')
    print("Received:\n ", body, "\nEnd")
    #print(method)
    channel.basic_ack(method.delivery_tag, False)
    # acking the message manually because why not
    #channel.basic_nack(method.delivery_tag,False, True)

#consuming / listening to a queu called my.queue1 and disabling auto_ack
channel.basic_consume(sys.argv[1], callback, False)

print(f"Waiting in queue -> {sys.argv[1]}")
#start consuming/
channel.start_consuming()
