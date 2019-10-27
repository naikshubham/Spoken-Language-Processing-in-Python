import wave

# create audio file wave object
good_morning = wave.open('../data/good_morning.wav', 'r')

# read all frames from wave object
signal_gm = good_morning.readframes(-1)

# view first 10
print(signal_gm[:10])