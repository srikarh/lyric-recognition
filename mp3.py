from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from azapi import AZlyrics
import speech_recognition as sr
from os import path
from pydub import AudioSegment



"""
src = "Lil Nas X - Panini.mp3"
dst = "audio_file.wav"

                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
"""

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "foreground.wav")


# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file
    
# recognize speech using Sphinx
try:
    print(r.recognize_sphinx(audio))
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