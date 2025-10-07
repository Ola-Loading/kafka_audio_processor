from Utils.consumer import main_consumer
from Utils.consumer_translate import consumer_translate
from Utils.producer import main_producer
import time
from multiprocessing import Process, Queue
import streamlit as st
import subprocess 
from kafka import KafkaConsumer
import threading 



st.set_page_config(page_title="Audio_Processor", page_icon=":material/waving_hand:")
st.title("🎙️ Transcribe and Translate Your Audio")

st.write("""
This app captures audio, transcribes it with OpenAI Whisper, and translates it using DeepL.
""")



def audio_process(consumer_output, translate_output):

    # consumer_output = Queue()
    # translate_output = Queue()

  
    consumer_process = Process(target=main_consumer,args=(consumer_output,))
    consumer_process.start()
    

    time.sleep(0.5)  # Ensure the consumer starts first

    producer_process = Process(target=main_producer)
    producer_process.start()

    translate_process = Process(target=consumer_translate,args=(translate_output,))
    translate_process.start()

    producer_process.join()
    consumer_process.join()
    translate_process.join()
    
    # transcription = consumer_output.get()
    # translations = translate_output.get()

    # return transcription, translations


# -- Kafka log consumer thread --
def stream_logs_live(log_container, stop_flag):
    consumer = KafkaConsumer(
        "logs",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="latest",
        group_id=None,
        consumer_timeout_ms=100  # quick timeout for looping
    )

    logs = []
    while not stop_flag["stop"]:
        for msg in consumer:
            log_line = msg.value.decode("utf-8")
            logs.append(log_line)
            log_container.text("\n".join(logs))
            if stop_flag["stop"]:
                break
        time.sleep(0.2)  # avoid tight loop

    consumer.close()

    
if st.button("Start Audio Processing"):
    # Setup communication queues
    consumer_output = Queue()
    translate_output = Queue()

    # Create log display area
    st.subheader("📡 Live Logs")
    log_placeholder = st.empty()

    # Use flag to stop log thread
    stop_flag = {"stop": False}
    log_thread = threading.Thread(target=stream_logs_live, args=(log_placeholder, stop_flag))
    log_thread.start()

    with st.spinner("Recording and processing audio..."):
        try:
            audio_process(consumer_output, translate_output)
        finally:
            stop_flag["stop"] = True
            log_thread.join()

    # Display results
    transcription = consumer_output.get()
    translations = translate_output.get()

    st.success("✅ Audio processing complete!")

    st.subheader("📝 Transcription:")
    st.write(transcription)

    st.subheader("🌐 Translations:")
    for lang_code, translation in translations:
        st.markdown(f"**{lang_code.upper()}**: {translation}")

   