from confluent_kafka import Consumer, KafkaError

class KafkaConsumer:
    def __init__(self):
        # Correct configuration initialization
        self.consumer = Consumer({
            'bootstrap.servers': 'locahost:9092',
            'group.id': 'my_consumer_group',
            'auto.offset.reset': 'earliest'
        })
        self.topic = 'energy'

    def consume_messages(self):
        # Subscribe to the topic
        self.consumer.subscribe([self.topic])

        while True:
            msg = self.consumer.poll(1.0)  # Poll for messages, timeout 1 second

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(msg.error())
                    break

            # Print the received message value
            print('Received message: {}'.format(msg.value().decode('utf-8')))

# Create an instance of the KafkaConsumer class
consumer_obj = KafkaConsumer()

# Start the consumer loop
consumer_obj.consume_messages()
