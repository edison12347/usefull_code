import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# export GOOGLE_APPLICATION_CREDENTIALS="/home/ed/Work/usefull_code/speech-recognition/key/chu-dev-5f449a6c1a98.json"
# ffmpeg -i stereo.flac -ac 1 mono.flac

def implicit():
    print('----->Works')
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'audio',
        'mono.flac')
    print('----->%s',file_name )

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_quickstart]
        with open("text/mono.txt", "w") as text_file:
            print(result.alternatives[0].transcript, file=text_file)

if __name__ == '__main__':
    implicit()