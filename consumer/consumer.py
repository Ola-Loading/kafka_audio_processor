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




def consume_audio_stream(topic='audio_events', output_file='received_audio.mp3'):
    """
    Consumes audio chunks from Kafka and reconstructs the audio file as mp3.
    
    :param topic: Kafka topic to consume audio data from.
    :param output_file: Path to save the reassembled mp3 file.
    """
    sample_format = pyaudio.paInt16  # 16-bit format
    channels = 2  # Stereo
    fs = 44100  # Sample rate (CD quality)

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',  # Start from the latest messages
        enable_auto_commit=True,
    )

    print("Listening for audio chunks...")
    p = pyaudio.PyAudio()
    frames = []

    for message in consumer:
        if message.value == b"end":
            break
        else:
            frames.append(message.value)
            print(f"Received chunk of size {len(message.value)} bytes")

      # Write MP3 binary data
    with open(output_file, 'wb') as f:
        f.write(b''.join(frames))

    print(f"MP3 file reconstructed: {output_file}")
    return output_file


def play_audio_transcribe(file_path):
    """Plays MP3, and transcribes."""

    #play MP3 File
    try:
        sound = AudioSegment.from_mp3(file_path)
        play(sound)
        print(f"Recording saved as {file_path}")

        # Transcribe using Whisper (optional)
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        print("Transcription:", result["text"])

        return (file_path,result)

    except Exception as e:
        print(f"Error processing audio: {e}")
        return str(e)

def translate_text(result):
    """Translates transcribed text into multiple languages."""
    load_dotenv()  # Loads variables from .env
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    deepl_client = deepl.DeepLClient(auth_key)
    detectlanguage.configuration.api_key = os.getenv("DETECT_LANG_KEY")
    language_dict = {'l1':'EN-GB','l2':'FR','l3':'PT-BR'}
    clone = dict(language_dict)
    detected_langs = detectlanguage.detect(result["text"])
    detected_lang = max(detected_langs, key=lambda x: x['confidence'])['language'].upper()
    
    try:
        # Remove detected language from translation list
        language_dict = {k: v for k, v in language_dict.items() if detected_lang not in v}
        
        translated = []
        for lang_code in language_dict.values():
            translated_text = deepl_client.translate_text(result["text"], target_lang=lang_code)
            translated.append((lang_code, translated_text))
            print(f"Translation ({lang_code}): {translated_text}")
        
        return translated
    except Exception as e:
        return str(e)


    

# Example usage
def main_consumer():
    mp3_file = consume_audio_stream()  # Receive and reconstruct audio
    playable_audio = play_audio_transcribe(mp3_file)  # Convert, play, and transcribe
    translate_text(playable_audio[1])

