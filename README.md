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

### The AudioFile class

```python
import speech_recognition as sr

# setup recognizer instance
recognizer = sr.Recognizer()

# read in audio file
clean_support_call = sr.AudioFile('clean.wav')

# check type of clean_support_call
type(clean_support_call)

# convert from audiofile to audiodata
with clean_support_call as source:
    # record the audio
    clean_support_call_audio = recognizer.record(source)

# transcribing our AudioData
recognizer.recognize_google(audio_data=clean_support_call_audio)
```

#### Duration and offset
- `Duration` and `offset` both None by default
- The record method records up to duration seconds of audio from source starting at offset. They are both set to None by default.
- This means that by default, record will record from the beginning of the file until there is no more audio. We can change this by setting them to a float value.
- For e.g, if we wanted the first 2 secs of all our audio files, we could set duration to 2. 
- The `offset parameter` can be used to cut off or skip over a specified amount of seconds at the start of an audio file.

```python
# leave duration and offset as default
with clean_support_call as source:
    clean_support_call_audio = recognizer.record(source, duration=None, offset=None)
    
# get first 2-secs of clean support call
with clean_support_call as source:
    clean_support_call_audio = recognizer.record(source, duration=2.0)
```














### Visualizing sound waves
- New audio file : good_afternoon.wav, we will plot both the sound waves and observe the difference between them. Both the good morning and good afternoon audio files are 48khz or 48000 frames per second
- Having audio files at the same frame rate and ensuring the dame data transformation are made on each of them is important. This is bcz if they are different, we have got the potential for data mismatches, which will prevent us from further processing.
- Same data transformations are done on good_afternoon file

#### Setting up a plot

```python
import matplotlib.pyplot as plt
plt.title('Good morning vs Good afternoon')

# x and y labels
plt.xlabel("Time (sec)")
plt.ylabel("Amplitude") # amplitude - or how much the sound wave displaces air particles as it moves through the air. A value of 0 indicates no sound at all

# add sound wave values
plt.plot(time_ga, soundwave_ga, label = "Good Afternoon")
plt.plot(time_gm, soundwave_gm, label = "Good Morning", alpha=0.5)

plt.legend()
plt.show()
```

- in the beginning, two sound waves are similar where the word 'good' would be but they begin to differ as morning and afternoon gets uttered

### SpeechRecognition Python library
- Some existing python libraries **CMU Sphinx, Kaldi, SpeechRecognition, Wav2letter++by Facebook**

#### Using the Recognizer class from SpeechRecognition

```python
# import the speech recognition library
import speech_recognition as sr

# create an instance of recognizer
recognizer = sr.Recognizer()

# set the energy threshold
# the energy threshold can be thought of as the loudness of audio which is considered speech, values below the threshold are considered as silence, values above are considered speech.A silent room is beetween 0 to 100
# SpeechRecognition documentation recommends 300 as a starting value which covers most speech files

recognizer.energy_threshold = 300
```

#### Using the Recognizer class to recognize speech
- Recognizer class has built-in functions which interact with speech APIs, `recognize_bing()` accesses Microsoft's cognitive services, `recognize_google()` uses Google's free web speech API, `recognize_google_cloud()` accesses Google's cloud speech API, `recognize_wit()` uses the wit.ai platform.
- They all accept an audio file and return text, which is hopefully the transcribed speech from the audio file

#### SppechRecognition Example
- Focus on `recognize_google`
- Recognize speech from an audio file with SpeechRecognition

```python
import SpeechRecognition as sr

recognizer = sr.Recognizer()

recognizer.recognize_google(audio_data=audio_file, language="en-US")
```








































