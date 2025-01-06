from kafka import KafkaConsumer
import boto3
import json

# Kafka Configuration
kafka_brokers = ['localhost:29092']  # Replace 'kafka' with 'localhost' if running outside Docker
kafka_topic = 'postgres.public.purchase_trends'  # Kafka topic for purchase_trends
consumer_group = 'python-consumer-group'  # Unique consumer group name

# AWS S3 Configuration
aws_access_key = ""
aws_secret_key = ""
s3_bucket_name = ""
s3_file_key = ""  # File path in the S3 bucket

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_brokers,
    auto_offset_reset='earliest',  # Start reading from the earliest message
    enable_auto_commit=True,
    group_id=consumer_group
)

# Initialize S3 Client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

print(f"Listening to Kafka topic: {kafka_topic} on brokers: {kafka_brokers}")

# Collect and Process Messages
messages = []
for message in consumer:
    # Decode the message
    decoded_message = message.value.decode('utf-8')
    print(f"Key: {message.key}, Value: {decoded_message}")
    messages.append(json.loads(decoded_message))  # Parse as JSON
    
    # Stop after processing a batch of messages (e.g., 10 messages)
    if len(messages) >= 10:
        break

# Combine messages into a JSON array
data_to_upload = json.dumps(messages, indent=4)

# Upload to S3
try:
    s3.put_object(Bucket=s3_bucket_name, Key=s3_file_key, Body=data_to_upload)
    print(f"Uploaded {len(messages)} messages to S3 bucket {s3_bucket_name} with key {s3_file_key}")
except Exception as e:
    print(f"Error uploading to S3: {e}")