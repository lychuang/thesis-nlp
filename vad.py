'''
VAD test script

- find duration of utterances using voice activity detection

'''

import collections
import contextlib
import sys
import wave

import webrtcvad

import numpy as np
import matplotlib.pyplot as plt
import json
from operator import itemgetter


def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate




class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration





def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n






def vad_collector(sample_rate, frame_duration_ms,
                  padding_duration_ms, vad, frames):
    """Filters out non-voiced audio frames.
    Given a webrtcvad.Vad and a source of audio frames, yields only
    the voiced audio.
    Uses a padded, sliding window algorithm over the audio frames.
    When more than 90% of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until 90% of the frames in
    the window are unvoiced to detrigger.
    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.
    Arguments:
    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).
    Returns: A generator that yields PCM audio data.
    """


    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False

    voiced_frames = []

    utt_durations = []

    duration = 0
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            # If we're NOTTRIGGERED and more than 90% of the frames in
            # the ring buffer are voiced frames, then enter the
            # TRIGGERED state.
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                #sys.stdout.write('+(%s)' % (ring_buffer[0][0].timestamp,))
                # We want to yield all the audio we see from now until
                # we are NOTTRIGGERED, but we have to start with the
                # audio that's already in the ring buffer.
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()

                duration += ring_buffer.maxlen * frame_duration_ms

        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])

            duration += frame_duration_ms

            # If more than 90% of the frames in the ring buffer are
            # unvoiced, then enter NOTTRIGGERED and yield whatever
            # audio we've collected.
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                #sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                triggered = False
                #yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []

                utt_durations.append(duration)
                duration = 0

    if triggered:
        #sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
        print("here")
    #sys.stdout.write('\n')
    # If we have any leftover voiced audio when we run out of input,
    # yield it.
    #if voiced_frames:
        #yield b''.join([f.bytes for f in voiced_frames])


    return utt_durations


def get_durations_wav(filename):
	
	audio, sample_rate = read_wave("audiosources/%s" % filename)
	vad = webrtcvad.Vad(2)
	frames = frame_generator(30, audio, sample_rate)
	frames = list(frames)
	durs = vad_collector(sample_rate, 30, 300, vad, frames)
	print(durs, len(durs))
	return durs

def get_durations_pcm(filename):

	file = open("audiosources/%s" %filename, "rb")

	audio = file.read()

	sample_rate = 16000
	vad = webrtcvad.Vad(2)
	frames = frame_generator(30, audio, sample_rate)
	frames = list(frames)
	durs = vad_collector(sample_rate, 30, 300, vad, frames)
	print(durs, len(durs))
	return durs



'''
This creates an alphabet of symbols based on an alphabet size
'''
def symboliser(length):


	symbol = chr(ord('A') + length)
	'''
	else:
		symbol = chr(ord('A') + 50 // incr)
	'''
	return symbol


def symbolise(filename):
	#filename = "Higa reveal.wav"
	#filename = "nfl2.pcm"

	if filename.split('.')[1] == "pcm":
		durs = get_durations_pcm(filename)

	elif filename.split('.')[1] == "wav":
		durs = get_durations_wav(filename)


	count = 0
	maxi = 121 # The highest utt duration?
	bins = np.zeros(maxi) # INIT the bins
	outputstring = ''

	sec_list = [durs[i] // 1000 for i in range(len(durs))]

	for i,d in enumerate(sec_list):
		#print(count, sent)


		secs = d

		if secs >= maxi:
			secs = maxi - 1
			sec_list[i] = secs


		outputstring += symboliser(secs)

		bins[secs] += 1
		#lengths.append(secs)

		#print (words)
		count += 1

	print(sec_list)


	#symbols = [i for i in range(maxi)]

	#bounds = [0, 3, 6, 10, 15, 20, 30, 40, 50, 60, 90, maxi - 1, maxi]

	#bounds = [0, 5, 10, 15, 20, 30, 40, 50, 60, 75, 90, 105, maxi - 1, maxi]
	bounds = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, maxi - 1, maxi]
	#bounds = [0, 2, 4, 7, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, maxi - 1, maxi]
	symbols = bounds


	#store the symbol : count
	symbdict = {}
	histo = []
	LUT = []
	'''
	This histogram accounts for the window size - assigns to a symbol
	'''
	for i in range(len(symbols) - 1):

		lower = symbols[i]
		upper = symbols[i+1]
		total = sum(bins[lower:upper])
		symb = chr(ord('A') + i)

		for j in range(upper):
			LUT += symb

		symbdict[symb] = [(lower,upper), total]


	print(symbdict)
	print(LUT)
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



	outputstring = ""
	for dur in sec_list:
		outputstring += LUT[dur]

	print(outputstring)
	print(len(outputstring))


	fname = filename.split(".")[0]

    #write symbols to file

	out = open("uttDurSYMB/%s.txt" % fname, 'w')
	out.write(outputstring)
	out.close()



	'''

	plt.hist(sec_list, bins=symbols)
	plt.title("%s Utterance Durations" % fname)
	plt.xlabel("Duration (seconds)")
	plt.xticks(symbols)
	plt.show()


	fig1, ax1 = plt.subplots()
	ax1.plot(ranks, [a[1]/count for a in ranked])
	ax1.set_title("Ranked Distribution %s" % fname)
	ax1.set_xlabel("Rank")
	#ax1.set_xscale('log')
	ax1.set_ylabel("Probability")

	plt.show()
    '''
