'''
Phoneme Symboliser Function

input -> path of audio file wav or pcm

writes symbolic output to txt file in phoneSYMB folder with same filename.txt

'''


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






def symbolise(filename):


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


	stream = open("audiosources/%s" % filename, 'rb')
	start_time = time.time() #timer for reference


	# CONFIGURE THE DECODER BASED ON ABOVE SETTINGS
	decoder = Decoder(config)

	# INIT THE BUFFER OF PHONEMES TO STORE
	phones_list = []


	#LOOP THOUGH UTTERANCES EXTRACTING PHONEMES, STORE IN phones_list each loop
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

	# FINISHED DECODING

	print("----------------- %s seconds -----------------" % (time.time() - start_time))

	hypothesis = decoder.hyp()
	print(phones_list, len(phones_list))


	# LIST OF PHONEMES FROM SPHINX
	PHONEMES = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'SIL', 'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH']
		
	P_symbolised = {} #THIS STORES {PHONEME : SYMBOL} MAPPING

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





	#GENERATE THE OUTPUT STRING OF SYMBOLS
	output = ''

	for i in phones_list:

	    if i in PHONEMES:
	        symb = P_symbolised[i][0]
	        output +=  symb

	print(output)

	fname = filename.split('.')[0] #EXTRACT THE FIRST PART OF FILENAME


	out = open("phoneSYMB/%s.txt" % fname, 'w')
	out.write(output)
	out.close()

	print("DONE HERE")