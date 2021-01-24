#importing pika    
import sys    
import pika    
     
#saving credentials to access the rabbitmq server    
credentials = pika.PlainCredentials(username='guest', password='guest')    
     
     
#establishing connection to rabbitmq server    
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.6.0.7', credentials=credentials))    
     
#establishing a channel to communicate with exchange    
channel = connection.channel()    

print("This is a SMS Gateway Server of Nepal")
     
#callback function which will be called on every new message on the queue.    
def callback(ch, method, properties , body):    
    body_str = body.decode('utf-8')    
    print(f"Sending message to {body_str}")
    print("Sent succesfully.")
    channel.basic_ack(method.delivery_tag, False)    
     
#consuming / listening to a queu called my.queue1 and disabling auto_ack    
channel.basic_consume("otp.gateway.nepal", callback, False)    
                                                                                                                                                                                              
print(f"Waiting in queue -> otp.gateway.nepal")                                                                                                                                                   
#start consuming/                                                                                                                                                                             
channel.start_consuming() 
