
import pika


#establishing connection with rabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.6.0.7'))

#creating a new channel for exchanging messages.
channel = connection.channel()

#declaring a new exchange to produce traffic into
channel.exchange_declare("ex.fanout", "fanout",durable=True, auto_delete=False )

#declaring two queues to send messages.
channel.queue_declare(queue='my.queue2', durable=True,exclusive=False, auto_delete=False)

channel.queue_declare(queue='my.queue1', durable=True,exclusive=False, auto_delete=False)

#binding queues to the exchange.
channel.queue_bind("my.queue1", "ex.fanout", "")
channel.queue_bind("my.queue2", "ex.fanout", "")

#publishing message to the exchange
print("Connection is ready [ send end to quit ]")
msg = ""
while msg != "end":
    msg = input("Enter your message: ")
    msg_en = msg.encode('utf-8')
    channel.basic_publish("ex.fanout", "", msg_en )

#waiting to check on consumer before removing the queue and exchange.

#cleaning all queues and exchanges
channel.queue_delete("my.queue1");
channel.queue_delete("my.queue2");

channel.exchange_delete("ex.fanout");

channel.close();
connection.close();

#checking if all works.
print("Deleted all messages")


