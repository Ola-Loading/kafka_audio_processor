from consumer.consumer import main_consumer
from producer.producer import main_producer
import time
from multiprocessing import Process

if __name__ == "__main__":
    consumer_process = Process(target=main_consumer)
    consumer_process.start()

    time.sleep(2)  # Ensure the consumer starts first

    producer_process = Process(target=main_producer)
    producer_process.start()

    producer_process.join()
    consumer_process.join()
