from nltk import tokenize
import numpy as np
import matplotlib.pyplot as plt

import re

import sentence_split as ss
import os
from os import environ, path
import json
from operator import itemgetter
import sys
print(sys.path)

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *


import speech_recognition as sr
from google.cloud import speech_v1p1beta1 as speech
import io

#from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types





def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    client = speech.SpeechClient.from_service_account_json(
        '/Users/lachlanhuang/Documents/2019/Thesis/thesis-service-key.json')

#explicit()

#client = speech.SpeechClient()


def transcribe(filename):

    client = speech.SpeechClient.from_service_account_json(
    	'/Users/lachlanhuang/Documents/2019/Thesis/thesis-service-key.json')


    audio = speech.types.RecognitionAudio(uri="gs://lachlan-thesis-audio/%s" % filename)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        # Enable automatic punctuation
        enable_automatic_punctuation=True)


    #response = client.recognize(config, audio)


    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=3600)

    transcribed = []

    fname = filename.split('.')[0]

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for i, result in enumerate(response.results):
        # The first alternative is the most likely one for this portion.
    	print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    	print('Confidence: {}'.format(result.alternatives[0].confidence))

    	text_file = open("textsources/%s.txt" % fname, "a")
    	text_file.write(result.alternatives[0].transcript)
    	text_file.close()



    return fname + ".txt"

    '''
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Sphinx
    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    '''
