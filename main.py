from consumer.consumer import main_consumer
from consumer_translate.consumer_translate import consumer_translate
from producer.producer import main_producer
import time
from multiprocessing import Process



if __name__ == "__main__":
    consumer_process = Process(target=main_consumer)
    consumer_process.start()
    

    time.sleep(0.5)  # Ensure the consumer starts first

    producer_process = Process(target=main_producer)
    producer_process.start()

    translate_process = Process(target=consumer_translate)
    translate_process.start()

    producer_process.join()
    consumer_process.join()
    translate_process.join()
