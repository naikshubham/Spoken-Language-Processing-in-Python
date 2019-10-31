# Spoken-Language-Processing-in-Python

## Load transform and transcribe audio files.

### Audio data in Python

#### Different kinds of audio files
- mp3
- wav
- m4a
- flac

- Digital sound is measured in frequency(kHz).
- Sampling rate of an audio file is the measure of the number of data change per second used to represent a digitial sound.
- 1kHz = 1000 pieces of information per second
- Streaming songs have a frequency of 32kHz (32k pieces of information per second)
- Audiobooks and spoken language are between 8 and 16kHz.
- Audio files are different from tabular or text data, because we can't immediately see the data we are working with. So we have to transform them first.

### Python builtin `wave` module for audio files

```python
import wave

# import audio file as wave object
good_morning = wave.open("good-morning.wav", "r")

# convert the wave object to bytes (-1 means read all the info in the file)
good_morning_soundwave = good_morning.readframes(-1)

# view the wav file in byte form
good_morning_soundwave

b`\xfd\xff\xfb\xff\xf8\xff\xf7\...`
```
- Files is 48kHz which means 48k pieces of information and 2 seconds long means 96k pieces of information

### Working with audio is different
- Have to convert the audio to something useful.
- Even a small sample of audio can contain large amount of information (adding background noise, other speakers)

### Converting sound wave bytes to integers using `numpy`

```python
import numpy as np

# convert soundwave_gm from bytes to integers
signal_gm = np.frombuffer(soundwave_gm, dtype='int16')

# frombuffer converts a series of data into a 1-D array

# show first 10 items
signal_gm[:10]
```
- Frequency is the measure of information per second, our soundwave has a freq of 48kHz and 2 seconds long and thus 96k pieces of information.

### Finding the frame rate
- Frequency(hz) = length of wave object array/duration of audio file(seconds)
- calling `getframerate()` on wave objec would return its framerate

```python
# get the frame rate
framerate_gm = good_morning.getframerate()
```

- Duration of audio file(sec) = length of wave object array / frequency(Hz)

### Finding sound wave timestamps
- we can use `np.linspace` to figure the timestamp where each soundwave value occurs.

```python
# return evenly spaced values between start and stop
np.linspace(start=1, stop=10, num=10)

# get the timestamps of the good morning sound wave
time_gm = np.linspace(start=0,
                      stop=len(soundwave_gm)/framerate_gm,
                      num=len(soundwave_gm))
```




















```




























