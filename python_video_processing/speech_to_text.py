# For extracting text from audio:
# Install the SpeechRecognition.
# In Terminal run the command:
# - (sudo) - pip install pyaudio
# - (sudo) pip install SpeechRecognition
#
# If it gives an error then first install:
# - sudo apt-get install python-pyaudio
# - sudo apt-get install libjack-jackd2-dev portaudio19-dev
#
# http://stackoverflow.com/questions/34733871/attributeerror-recognizer-object-has-no-attribute-recognize

import speech_recognition as sr

r = sr.Recognizer()
with sr.WavFile("audio/audio.wav") as source:          # use "test.wav" as the audio source
    audio = r.record(source)                      # extract audio data from the file

try:
    print("Transcription: " + r.recognize_google(audio))   # recognize speech using Google Speech Recognition
except LookupError:                                 # speech is unintelligible
    print("Could not understand audio")
