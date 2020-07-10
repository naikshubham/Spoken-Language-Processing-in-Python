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

#### SpeechRecognition Example
- Focus on `recognize_google`
- Recognize speech from an audio file with SpeechRecognition

```python
import SpeechRecognition as sr

recognizer = sr.Recognizer()

recognizer.recognize_google(audio_data=audio_file, language="en-US")
```

### Dealing with different kinds of audio
- Although SpeechRecognition is capable of transcribing audio, it doesn't necessarily know what kind of audio it's transcribing.
- For e.g, if we pass recognizer an audio file with Japanese speech but the language tag was English US, we'd get back the Japanese audio in English characters.

```python
recognizer = sr.Recognizer()

# pass the japanese audio to recognize google
text = recognizer.recognize_google(japanese_good_morning, langauge='en-US')

print(text)
```

- And if we passed the same audio file with the language tag set to `ja` for japanese, we'd get the audio transcribed into Japanese characters. The thing to note is SpeechRecognition library doesn't automatically detect languages. So we have to ensure this parameter is set manually and make sure the API we are using has the capability to transcribe the language the audio files are in.

#### Non-speech audio
- If we pass SpeechRecognition an audio file of a leopard roaring, it would return an unknown value error because no speech was detected. Bcz isn't human speech. We can prevent errors by using the show all parameter.
- The show all parameter shows a list of all the potential transcriptions the recognize google function came up with. In case of the leopard roar, the list comes back empty but we avoid raising an error.
- Or in the case of Japanese file ,we will see the different potential transcriptions.

```python
# recognizing japanese audio with show_all=True

text = recognizer.recognize_google(japanese_audio, language="en-US", show_all=True)

print(text)
```

#### Multiple speakers
- The process of splitting more than one speaker from a single audio file is called **speaker diarization**.

#### Noisy audio
- If we have trobule hearing the speech, so will the APIs.
- To try and accomadate for background noise, the recognizer class has a built-in function `adjust_for_ambient_noise`, which takes a parameter `duration`.
- The recognizer class then listens for duration seconds at the start of the audio file and adjusts the energy threshold, or the amount the recognizer class listens, to a level suitable for the background noise.
- How much space we have at the start of the audio file will dictate what we can set the duration value to. Documentation suggests a value between 0.5 - 1 sec.

```python
noisy_support_call = sr.AudioFile(noisy_support_call.wav)

with noisy_support_call as source:
    # adjust for ambient noise and record
    recognizer.adjust_for_ambient_noise(source, duration=0.5)
    noisy_support_call_audio = recognizer.record(source)

# record the audio
recognizer.recognize_google(noisy_support_call_audio)
```

### PyDub
- Works well with `.wav`, needs `ffmpeg` for other formats like `mp3`

#### PyDub's main class, AudioSegment

```python
from pydub import AudioSegment

# import an audio file # format is only for readability, as it gets inferred from the audio file name
wav_file = AudioSegment.from_file(file="wav_file.wav", format="wav")
```

#### Playing an audio file
`pip install simpleaudio`

```python
from pydub.playback import play

# import audio file
wav_file = AudioSegment.from_file(file="wav_file.wav")

# play the audio file
play(wav_file)
```

#### Audio parameters

```python
# pydub automatically infers number of parameters from the file
wav_file = AudioSegment.from_file(file="wav_file.wav")
two_speakers = AudioSegment.from_file(file="two_speakers.wav")

# check for number of channels
wav_file.channels, two_speakers.channels
wav_file.frame_rate

# find the number of bytes per sample
wav_file.sample_width
wav_file.max
```

- Example, callig channels on AudioSegment will show us the number pf channels, 1 for mono, 2 for stereo audio.
- Calling frame rate gives us the sample of our AudioSegment in Hertz.
- sample_width tells us the no of bytes per sample. 1 means 8-bit, 2 means 16-bit
- max will tell us the max amplitude of our audio file, which can be considered loudness and is useful for normalizing sound levels.

#### Changing audio parameters
- We can adjust them using set attribute name style functions like set sample width to adjust the sample width.

```python
# change ATTRIBUTENAME of AudioSegment to x
changed_audio_segment = audio_segment.set_ATTRIBUTENAME(x)

# change sample width to 1
wav_file_width_1 = wav_file.sample_width(1)
wav_file_width_1.sample_width

# change sample rate
wav_file_16k = wav_file.set_frame_rate(16000)
wav_file_16k.frame_rate

# change number of channels
wav_file_1_channel = wav_file.set_channels(1)
wav_file_1_channel.channels
```

- Some APIs require our audio files to have certain values for these parameters. 
- A rule of thumb is the higher the values, excluding channels, the better.
- We should aim for a minimum of 16khz as the frame rate and to have our audio files in wav format.































