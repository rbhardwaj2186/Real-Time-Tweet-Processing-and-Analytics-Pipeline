# Import necessary libraries
from kafka import KafkaConsumer
from json import loads
from rich import print
from hdfs import InsecureClient

# Create a Kafka consumer
consumer = KafkaConsumer(
    'my-topic-test',  # Topic to consume messages from
    bootstrap_servers=['localhost:9092'],  # Kafka server addresses
    auto_offset_reset='earliest',  # Reset offset to the earliest available message
    enable_auto_commit=True,  # Enable auto commit of consumed messages
    group_id=None,  # Consumer group ID (None indicates an individual consumer)
    value_deserializer=lambda x: loads(x.decode('utf-8'))  # Deserialize the message value from JSON to Python object
)

# Initialize HDFS Client
client = InsecureClient('http://VPS-DATA1:50070')  # Use HDFS web interface port (50070 by default)
hdfs_path = '/kafka_demo/tweets_data.json'  # Relative path to the file on HDFS

# Process incoming Kafka messages
for message in consumer:
    tweet = message.value  # Get the value of the message (tweet)
    print(tweet)  # Print the tweet

    # Append the tweet to the HDFS file
    with client.write(hdfs_path, append=True, encoding='utf-8') as file:
        print("Storing in HDFS!")
        file.write(f"{tweet}\n")
