from kafka import KafkaConsumer
import os
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import whisper
import deepl
from dotenv import load_dotenv
import os
import detectlanguage 




def consume_transcript(topic='transcriptions'):
    """
    Consumes transcribed text from a kafka topic 'transcriptions'.

    :param topic: Kafka topic to consume data from.

    """
  

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',  # Start from the latest messages
        enable_auto_commit=True,
        value_deserializer=lambda v: v.decode('utf-8')
    )

    print("Listening for text...")
   
    frames = []

    counter = 0

    for message in consumer:
        if message.value== "end":
            break
        else:
            frames.append(message.value)
            print(f"Received chunk of size {len(message.value)} bytes")
            
    return frames[0]


def translate_text(result):
    """Translates transcribed text into multiple languages."""
    load_dotenv()  # Loads variables from .env
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    deepl_client = deepl.DeepLClient(auth_key)
    detectlanguage.configuration.api_key = os.getenv("DETECT_LANG_KEY")
    language_dict = {'l1':'EN-GB','l2':'FR','l3':'PT-BR'}
    clone = dict(language_dict)
    detected_langs = detectlanguage.detect(result)
    detected_lang = max(detected_langs, key=lambda x: x['confidence'])['language'].upper()
    
    try:
        # Remove detected language from translation list
        language_dict = {k: v for k, v in language_dict.items() if detected_lang not in v}
        
        translated = []
        for lang_code in language_dict.values():
            translated_text = deepl_client.translate_text(result, target_lang=lang_code)
            translated.append((lang_code, translated_text))
            print(f"Translation ({lang_code}): {translated_text}")
        
        return translated
    except Exception as e:
        return str(e)


    

# Example usage
def consumer_translate():
    text = consume_transcript() # Receive and save transcript
    translate_text(text)

