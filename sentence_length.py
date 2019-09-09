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






MODELDIR = "/usr/local/lib/python3.7/site-packages/pocketsphinx/model/"
DATADIR = "/usr/local/lib/python3.7/site-packages/pocketsphinx/data/"








#HISTOGRAM window size??
incr = 2





'''
This creates an alphabet of symbols based on an alphabet size
'''
def symboliser(length):

	if length < 51:
		symbol = chr(ord('A') + length // incr)
	else:
		symbol = chr(ord('A') + 50 // incr)
	return symbol



def symbolise(filename):

	'''
	Get the string, split into array of sents
	'''
	#text = open("action_transcribed_combined.txt", 'r')
	text = open("textsources/%s" % filename, 'r')
	text = text.read()
	sents = ss.split_into_sentences(text)


	count = 0
	max = 300 # The highest sentence length?
	bins = np.zeros(max) # INIT the bins
	lengths = [] # list of lengths
	outputstring = ''

	'''
	Generate the histogram of sentence lenghts from sents array
	'''
	for sent in sents:
		#print(count, sent)
		words = len(re.findall(r'\w+', sent))

		outputstring += symboliser(words)

		bins[words - 1] += 1
		lengths.append(words)

		#print (words)
		count += 1

	print(bins)
	print("TOTAL SAMPLES: %d\n\n" % count)


	#init array of symbols
	symbols = [i for i in range(0, 52, incr)]
	s = [i for i in range(0, 50, 2)]

	#store the symbol : count
	symbdict = {}

	'''
	This histogram accounts for the window size - assigns to a symbol
	'''
	for i in range(len(symbols) - 1):

		lower = symbols[i]
		upper = symbols[i+1]
		total = sum(bins[lower:upper])
		symb = chr(ord('A') + i)

		symbdict[symb] = [(lower,upper), total]

	print(symbdict)


	'''
	CREATE A RANKED DISTRIBUTION
	'''
	ranked = []

	for sym in symbdict.keys():

		ranked.append((sym, symbdict[sym][1]))

	ranked.sort(key=itemgetter(1), reverse=True)
	print(ranked)

	ranks = [i for i in range(1,len(ranked) + 1)]
	print(ranks)


	print("\n\n", outputstring, "\n\n")


	out = open("uttSYMB/%s" % filename, 'w')
	out.write(outputstring)
	out.close()



	'''
	with open("actiondict2.json", 'w') as outfile:
	    json.dump(symbdict, outfile, indent=4, default=str)
	'''


	#PLOT
	'''
	plt.hist(lengths, bins=symbols)
	plt.title("Action Sent Length")
	plt.xlabel("Number of Words")
	plt.xticks(symbols)
	plt.show()

	fig1, ax1 = plt.subplots()
	ax1.plot(ranks, [a[1]/count for a in ranked])
	ax1.set_title("Ranked Distribution Action Conversations")
	ax1.set_xlabel("Rank")
	#ax1.set_xscale('log')
	ax1.set_ylabel("Probability")

	plt.show()
	'''