import vad 

import time


start_time = time.time()

files = ["peterpan1.wav", "peterpan2.wav", "Higa reveal.wav", "Higa dawson.wav", "Higa blogger.wav", "Higa bi.wav"]
'''
for f in files:
	vad.symbolise(f)
'''

for i in range(17):
	f = "peterpan%i.wav" % (i+1)
	vad.symbolise(f)



print("----------------- %s seconds -----------------" % (time.time() - start_time))