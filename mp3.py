from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from azapi import AZlyrics
import speech_recognition as sr
from os import path
from pydub import AudioSegment
import scipy.io.wavfile
import repet
import numpy as np
import matplotlib.pyplot as plt



src = "Lil Nas X - Panini.mp3"
dst = "audio_file.wav"

                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), dst)
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file


# Audio signal (normalized) and sample rate in Hz
sample_rate, audio_signal = scipy.io.wavfile.read('audio_file.wav')
print(str(sample_rate) + " " + str(audio_signal))
audio_signal = audio_signal / (2.0**(audio_signal.itemsize*8-1))

# Estimate the background signal and infer the foreground signal
background_signal = repet.original(audio_signal, sample_rate);
foreground_signal = audio_signal-background_signal;

# Write the background and foreground signals (un-normalized)
scipy.io.wavfile.write('background_signal.wav', sample_rate, background_signal)
scipy.io.wavfile.write('foreground_signal.wav', sample_rate, foreground_signal)

# Compute the audio, background, and foreground spectrograms
window_length = repet.windowlength(sample_rate)
window_function = repet.windowfunction(window_length)
step_length = repet.steplength(window_length)
audio_spectrogram = abs(repet._stft(np.mean(audio_signal, axis=1), window_function, step_length)[0:int(window_length/2)+1, :])
background_spectrogram = abs(repet._stft(np.mean(background_signal, axis=1), window_function, step_length)[0:int(window_length/2)+1, :])
foreground_spectrogram = abs(repet._stft(np.mean(foreground_signal, axis=1), window_function, step_length)[0:int(window_length/2)+1, :])


window_length = repet.windowlength(sample_rate)
window_function = repet.windowfunction(window_length)
step_length = repet.steplength(window_length)
audio_spectrogram = abs(repet._stft(np.mean(audio_signal, axis=1), window_function, step_length)[0:int(window_length/2)+1, :])
background_spectrogram = abs(repet._stft(np.mean(background_signal, axis=1), window_function, step_length)[0:int(window_length/2)+1, :])
foreground_spectrogram = abs(repet._stft(np.mean(foreground_signal, axis=1), window_function, step_length)[0:int(window_length/2)+1, :])

# Display the audio, background, and foreground spectrograms (up to 5kHz)
plt.rc('font', size=30)
plt.subplot(3, 1, 1)
plt.imshow(20*np.log10(audio_spectrogram[1:int(window_length/8), :]), aspect='auto', cmap='jet', origin='lower')
plt.title('Audio Spectrogram (dB)')
plt.xticks(np.round(np.arange(1, np.floor(len(audio_signal)/sample_rate)+1)*sample_rate/step_length),
        np.arange(1, int(np.floor(len(audio_signal)/sample_rate))+1))
plt.xlabel('Time (s)')
plt.yticks(np.round(np.arange(1e3, int(sample_rate/8)+1, 1e3)/sample_rate*window_length),
        np.arange(1, int(sample_rate/8*1e3)+1))
plt.ylabel('Frequency (kHz)')
plt.subplot(3, 1, 2)
plt.imshow(20*np.log10(background_spectrogram[1:int(window_length/8), :]), aspect='auto', cmap='jet', origin='lower')
plt.title('Background Spectrogram (dB)')
plt.xticks(np.round(np.arange(1, np.floor(len(audio_signal)/sample_rate)+1)*sample_rate/step_length),
        np.arange(1, int(np.floor(len(audio_signal)/sample_rate))+1))
plt.xlabel('Time (s)')
plt.yticks(np.round(np.arange(1e3, int(sample_rate/8)+1, 1e3)/sample_rate*window_length),
        np.arange(1, int(sample_rate/8*1e3)+1))
plt.ylabel('Frequency (kHz)')
plt.subplot(3, 1, 3)
plt.imshow(20*np.log10(foreground_spectrogram[1:int(window_length/8), :]), aspect='auto', cmap='jet', origin='lower')
plt.title('Foreground Spectrogram (dB)')
plt.xticks(np.round(np.arange(1, np.floor(len(audio_signal)/sample_rate)+1)*sample_rate/step_length),
        np.arange(1, int(np.floor(len(audio_signal)/sample_rate))+1))
plt.xlabel('Time (s)')
plt.yticks(np.round(np.arange(1e3, int(sample_rate/8)+1, 1e3)/sample_rate*window_length),
        np.arange(1, int(sample_rate/8*1e3)+1))
plt.ylabel('Frequency (kHz)')
plt.show()


dst = "foreground_signal.wav"
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), dst)
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))


"""
# Create MP3File instance.
mp3 = MP3File(src)

# Get all tags.

rawSong = mp3.song[0]

api = AZlyrics()

songstr = str(rawSong.value)


songs = api.search(songstr[0: len(songstr) - 1], category = 'songs')

# Song appears to be the first in search results
song_url = songs[0]['url']

Lyrics = api.getLyrics(url = song_url)

"""