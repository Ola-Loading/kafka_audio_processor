import pyaudio 
import time
import wave
import os
import numpy as np
from pydub import AudioSegment
from kafka import KafkaProducer
from kafka.errors import KafkaError

def read_audio_file(file_path): 
       with open(file_path, 'rb') as audio_file: 
           return audio_file.read() 

def send_audio_stream_to_kafka(snippet, topic='audio_events'):
    """
    Streams an MP3 file in chunks to a Kafka topic instead of loading it into memory.
    
    :param file_path: Path to the MP3 file.
    :param topic: Kafka topic to send the data to.
    :param chunk_size: Size of each chunk in bytes (default 64 KB).
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092'
        )
        with open(snippet, 'rb') as audio_file:
            while chunk := audio_file.read(65536):  # 64 KB chunks
                 producer.send(topic, value=chunk)
                 print("Sent chunk to Kafka")
        
        producer.send(topic, value=b"end")  # Send end marker

        print(f"Sent voice snippet to Kafka")

    except KafkaError as e:
        print(f"Kafka Error: {e}")

    finally:
        producer.flush()
        producer.close()

    os.remove(snippet)

def record_audio_as_wav(filename):
    chunk = 1024  # Number of audio samples per chunk
    sample_format = pyaudio.paInt16  # 16-bit format
    channels = 2  # Stereo
    fs = 44100  # Sample rate (CD quality)
    filename = filename
    silence_threshold = 500  # Adjust based on noise levels
    silence_duration = 2  # Stop after 2 seconds of silence

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    silent_chunks = 0
    time.sleep(2)
    print("Recording... Speak now!")

    while True:
        data = stream.read(chunk,exception_on_overflow = False)  # Read chunk of audio
        # send_audio_stream_to_kafka(data, topic='audio_events')
        
        frames.append(data)

        # Convert to numpy array to measure volume
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()  # Get average volume level

        if volume < silence_threshold:
            silent_chunks += 1
        else:
            silent_chunks = 0  # Reset silent chunk counter if sound is detected

        if silent_chunks > (fs / chunk * silence_duration):  # Stop if silent for `silence_duration` seconds
            print("Silence detected. Stopping recording.")

            break

    # Stop and close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

  # Save the audio
    wf = wave.open(filename+".wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Recording saved as", filename+".wav")
    
    return filename


def wav_to_mp3(filename):
    ''' Conversion for storage reasons. 
    MP3 files use lossy compression, reducing file size by up to 90% without significant quality loss.
    Also WAV files are not always supported on mobile devices, browsers, or online platforms, whilst
    MP3 is widely supported and works on almost all
'''
    
    AudioSegment.converter = "/usr/local/bin/ffmpeg"  # Adjust path if needed

    sound = AudioSegment.from_wav(filename+".wav")
    try:
        sound.export(filename+".mp3", format="mp3")
        os.remove(filename+".wav")
        print("Recording saved as", filename+".mp3")
        print("Recording deleted: ", filename+".wav")
        return filename+".mp3"

    except Exception as e:
        return str(e)
    


def main_producer():
    print('Wait for the onscreen prompt before you start speaking/playing audio. Please record in a noise-free environment...')

    filename = record_audio_as_wav('audio_file')   #Captures audio as a wave file using pyaudio library

    mp3_file = wav_to_mp3(filename)     #Takes file and saves as an mp3 which takes up less storage, is sufficiently high quality and is compatible with a host of devices

    send_audio_stream_to_kafka(mp3_file, topic='audio_events')
    
