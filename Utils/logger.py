
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092")

def log_to_kafka(message: str):
    producer.send("logs", message.encode("utf-8"))
    producer.flush()
