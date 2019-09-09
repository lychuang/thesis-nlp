from nltk import tokenize
import numpy as np
import matplotlib.pyplot as plt

import re
import time

import os
from os import environ, path
import json
from operator import itemgetter
import sys
print(sys.path)
sys.path.insert(0, "/usr/local/lib/python3.7/site-packages/")

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *


MODELDIR = "/usr/local/lib/python3.7/site-packages/pocketsphinx/model/"
DATADIR = "/usr/local/lib/python3.7/site-pAackages/pocketsphinx/data/"
MDIR = "/Users/lachlanhuang/Documents/2019/Thesis/pocketsphinx-5prealpha/model/en-us"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
config.set_string('-allphone', path.join(MODELDIR, 'en-us/en-us-phone.lm.dmp'))
config.set_string('-mdef', path.join(MDIR, 'en-us/mdef'))
config.set_string('-tmat', path.join(MDIR, 'en-us/transition_matrices'))
config.set_string('-mean', path.join(MDIR, 'en-us/means'))
config.set_string('-var', path.join(MDIR, 'en-us/variances'))
'''config.set_float('-lw', 2.0)
'''
config.set_float('-beam', 1e-20)
config.set_float('-pbeam', 1e-20)


stream = open('audiosources/actionselfdialogue_full.pcm', 'rb')



phones_list = []



start_time = time.time() #timer for reference

'''
buf = "hi"
# Decode streaming data.
decoder = Decoder(config)
MB = 0
while buf:
    decoder.start_utt()
    count = 0
    print("THIS IS THE COUNT: %d" % MB)
    MB += 1
    while count < 500:
        buf = stream.read(1024)
        count += 1
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break


    decoder.end_utt()
    print ('Phonemes: ', [seg.word for seg in decoder.seg()])
    phones_list_append = [seg.word for seg in decoder.seg()]
    phones_list += phones_list_append

    print(phones_list, len(phones_list))

'''
decoder = Decoder(config)


'''
p1 = Person("bob", 20, 'M')
p2 = Person("moo", 100, 'F')
age = p1.get_age() -> 20
age2 = p2.get_age() -> 100
'''


in_speech_bf = False
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                print ('Result:', decoder.hyp().hypstr)
                print ('Phonemes: ', [seg.word for seg in decoder.seg()])
                phones_list_append = [seg.word for seg in decoder.seg()]
                phones_list += phones_list_append
                decoder.start_utt()
    else:
        break
decoder.end_utt()



print("----------------- %s seconds -----------------" % (time.time() - start_time))




hypothesis = decoder.hyp()
#print ('Phonemes: ', [seg.word for seg in decoder.seg()])


print(phones_list, len(phones_list))



phonemes = list(set(phones_list))


PHONEMES = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'SIL', 'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH']
P_symbolised = {}

#print(len(PHONEMES))
'''
This creates an alphabet of symbols based on an alphabet size
'''
def symboliser(offset):

	symbol = chr(ord('A') + offset)
	return symbol

c = 0
for p in PHONEMES:

    P_symbolised[p] = [symboliser(c), c]
    c += 1

print(P_symbolised)
print(c)


#create the output string of symbols
output = ''

for i in phones_list:

    if i in PHONEMES:
        symb = P_symbolised[i][0]
        output +=  symb

print(output)

out = open("phoneSYMB/NEW_actionselfdialogue_full.txt", 'w')
out.write(output)
out.close()

print("DONE HERE")
