from consumer.consumer import main_consumer
from producer.producer import record_audio_as_wav
import time
from multiprocessing import Process


if __name__ == "__main__":
    consumer_process = Process(target=main_consumer)
    consumer_process.start()

    time.sleep(2)  # Ensure the consumer starts first
    record_audio_as_wav()

    consumer_process.join()