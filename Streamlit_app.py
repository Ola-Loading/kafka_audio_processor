from Utils.consumer import main_consumer
from Utils.consumer_translate import consumer_translate
from Utils.producer import main_producer
import time
from multiprocessing import Process, Queue
import streamlit as st


st.set_page_config(page_title="Audio_Processor", page_icon=":material/waving_hand:")
st.title("🎙️ Transcribe and Translate Your Audio")

st.write("""
This app captures audio, transcribes it with OpenAI Whisper, and translates it using DeepL.
""")



def audio_process():

    consumer_output = Queue()
    translate_output = Queue()

  
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
    
    transcription = consumer_output.get()
    translations = translate_output.get()

    return transcription, translations



if st.button("Start Audio Processing"):
    with st.spinner("Recording and processing audio..."):
        transcription, translations = audio_process()

    st.subheader("📝 Transcription:")
    st.write(transcription)

    st.subheader("🌐 Translations:")
    for lang_code, translation in translations:
        st.markdown(f"**{lang_code}**: {translation}")