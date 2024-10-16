import json
from kafka import KafkaProducer
from time import sleep
from rich import print

# Kafka Producer initialization
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda K: json.dumps(K).encode('utf-8')
)

# Simulate reading data from data.json
json_file_path = 'data.json'  # Update the path if necessary

with open(json_file_path, 'r') as file:
    for line in file:
        tweet_data = json.loads(line)
        # Access necessary fields from the tweet data
        cur_data = {
            "id_str": tweet_data['id_str'],
            "username": tweet_data['username'],
            "tweet": tweet_data['tweet'],
            "location": tweet_data['location'],
            "created_at": tweet_data['created_at'],
            "retweet_count": tweet_data['retweet_count'],
            "favorite_count": tweet_data['favorite_count'],
            "followers_count": tweet_data['followers_count'],
            "lang": tweet_data['lang'],
            "coordinates": tweet_data['coordinates']
        }

        # Send the tweet data to Kafka
        producer.send('my-topic-test', value=cur_data)
        print(f"Sent tweet: {cur_data}")
        sleep(0.5)  # Simulate a delay between sending messages