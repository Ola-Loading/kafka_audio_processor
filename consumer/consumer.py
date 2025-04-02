from kafka import KafkaConsumer
import os
import wave
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import whisper
import deepl
from dotenv import load_dotenv
import os
import detectlanguage 




def consume_audio_stream(topic='audio_events', output_file='received_audio.wav'):
    """
    Consumes audio chunks from Kafka and reconstructs the audio file as WAV.
    
    :param topic: Kafka topic to consume audio data from.
    :param output_file: Path to save the reassembled WAV file.
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

    # Save to WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

    print(f"Audio file reconstructed: {output_file}")
    return output_file


def play_audio_transcribe(file_path):
    """Converts WAV to MP3, deletes WAV, plays MP3, and transcribes."""
    
    # Ensure correct MP3 filename
    mp3_file = os.path.splitext(file_path)[0] + ".mp3"

    # Convert WAV to MP3
    try:
        sound = AudioSegment.from_wav(file_path)
        sound.export(mp3_file, format="mp3")
        os.remove(file_path)  # Delete WAV file after conversion
        print(f"Recording saved as {mp3_file}")
        print(f"Recording deleted: {file_path}")

        # Play MP3
        # audio = AudioSegment.from_mp3(mp3_file)
        # play(audio)

        # Transcribe using Whisper (optional)
        model = whisper.load_model("base")
        result = model.transcribe(mp3_file)
        print("Transcription:", result["text"])

        return (mp3_file,result)

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
    wav_file = consume_audio_stream()  # Receive and reconstruct audio
    playable_audio = play_audio_transcribe(wav_file)  # Convert, play, and transcribe
    translate_text(playable_audio[1])

