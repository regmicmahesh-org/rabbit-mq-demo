import pika


#establishing connection with rabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.6.0.7'))

#creating a new channel for exchanging messages.
channel = connection.channel()

#declaring a new exchange to produce traffic into
channel.exchange_declare("ex.direct", "direct",durable=True, auto_delete=False )

#declaring two queues to send messages.
channel.queue_declare(queue='my.errors', durable=True,exclusive=False, auto_delete=False)
channel.queue_declare(queue='my.warnings', durable=True,exclusive=False, auto_delete=False)
channel.queue_declare(queue='my.infos', durable=True,exclusive=False, auto_delete=False)

#binding queues to the exchange.
channel.queue_bind("my.errors", "ex.direct", "error")
channel.queue_bind("my.warnings", "ex.direct", "warning")
channel.queue_bind("my.infos", "ex.direct", "info")

#publishing message to the exchange
print("Connection is ready [ send end to quit ]")
msg = ""
routing_key = ""
while msg != "end":
    msg = input("Enter your message: ")
    routing_key = input("Enter your routing key [error/warning/info]: ")
    msg_en = msg.encode('utf-8')
    channel.basic_publish("ex.direct",routing_key, msg_en )

#waiting to check on consumer before removing the queue and exchange.

#cleaning all queues and exchanges
channel.queue_delete("my.warnings");
channel.queue_delete("my.errors");
channel.queue_delete("my.infos");

channel.exchange_delete("ex.direct");

channel.close();
connection.close();

#checking if all works.
print("Deleted all messages")