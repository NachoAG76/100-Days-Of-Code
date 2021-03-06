import datetime

title = input("\nInput a name for your audio recording file: ")
today_formatted = datetime.datetime.today().strftime("%m-%d-%Y")
name = f"{title}-audio-recording-{today_formatted}.wav"

samplerate = 44100
channels = 1

import queue
qu = queue.Queue()

def callback(audio_data, frames, time, status):
    if status:
        print(status)
    qu.put(audio_data.copy())
    
import sounddevice as sd
import soundfile as sf

try:
    with sf.SoundFile(name, mode="x", samplerate= samplerate, channels= channels) as f:
        with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
            print("\nRecording started.\nPress Ctrl+C to end recording\n")
            while True:
                f.write(qu.get())

except KeyboardInterrupt:
    print(f"\nRecording finished, audio file named {name} created.")
except Exception:
    print(Exception)

import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def transcribe(filename):
    client = speech.SpeechClient()
    file_name = os.path.join(filename)

    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=samplerate,
        language_code="en-US")

    # Detects speech in the audio file
    transcription = client.recognize(config, audio)

    print("\n")
    for i,result in enumerate(transcription.results):
        print(f"Transcription {i}: {result.alternatives[0].transcript}")
    print("\n")

transcribe(name)

