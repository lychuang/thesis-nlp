#phoneme histogram / plots

from nltk import tokenize
import numpy as np
import matplotlib.pyplot as plt

import re

import os
from os import environ, path
import json
from operator import itemgetter
import sys
print(sys.path)
sys.path.insert(0, "/usr/local/lib/python3.7/site-packages/")

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *


filename = "action500.txt"

phones = open(filename, 'r')
phones_text = phones.read()

phones_text = phones_text.strip('[]')
phones_text = phones_text.replace("'", "")
phones_list = phones_text.split(', ')

phoneme_set = set(phones_list)

phone_count = {}

for phone in phoneme_set:
    phone_count[phone] = 0


for p in phones_list:

    phone_count[p] += 1

print(phone_count)

ranked = []

for p in phone_count.keys():

	ranked.append((p, phone_count[p]))

ranked.sort(key=itemgetter(1), reverse=True)
print(ranked)

ranks = [i for i in range(1,len(ranked) + 1)]

count = len(phones_list)
print(count)
fig1, ax1 = plt.subplots()
ax1.plot(ranks, [a[1]/count for a in ranked])
ax1.set_title("Ranked Distribution Conversational Phonemes")
ax1.set_xlabel("Rank")
#ax1.set_xscale('log')
ax1.set_ylabel("Probability")

plt.show()
