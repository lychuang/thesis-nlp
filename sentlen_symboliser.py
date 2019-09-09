'''
SENTENCE LENGTH SYMBOLISING SCRIPT
'''


import transcribe_audio as tr
import sentence_length as sent

import time


start_time = time.time()

files = ["Higa-breakup.wav", "Higa-ghost.wav", "Higa-hate.wav", "Higa-hearthstone.wav", "Higa-raptors.wav", "Higa-ytf.wav"]
#bi blogger dawson reveal twilight youtube
for i in range(17):
	f = "peterpan%i.wav" % (i+1)
	#vad.symbolise(f)

	for attempt in range(4):
		try:
		  # do thing
			text = tr.transcribe(f)
			sent.symbolise(text)
		except:
		  # perhaps reconnect, etc.
			continue
		else:
			break
	


#text = tr.transcribe("Higa-breakup.wav")
#text = ".txt"











print("----------------- %s seconds -----------------" % (time.time() - start_time))