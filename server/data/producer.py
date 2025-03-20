import time
from faker import Faker
from confluent_kafka import Producer

fake = Faker()

class PushToKafka:
    def __init__(self):
        # Correct configuration initialization
        self.producer = Producer({"bootstrap.servers": "localhost:9092"})
        self.topic = 'energy'

    def insert_into_kafka(self, message):
        # Produce the message (convert string to bytes)
        self.producer.produce(topic=self.topic, partition=0, value=message.encode('utf-8'), callback=self.delivery_report)
        # Wait for any outstanding messages to be delivered and delivery reports to be received
        self.producer.flush()

    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Create an instance of the PushToKafka class
producer_obj = PushToKafka()

# Start the producer loop
while True:
    new_message = fake.text()
    producer_obj.insert_into_kafka(new_message)
    print('Produced new message: {}'.format(new_message))
    time.sleep(2)  # Sleep for 2 seconds between each message
