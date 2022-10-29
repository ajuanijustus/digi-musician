# Import libraries
import os

# Import from libraries
from midi2audio import FluidSynth
from pydub import AudioSegment

# Instantiate fluid synth
fs = FluidSynth()

# Constant name of file
MIDI_FILE = "major-scale"

# Gen path to file
path = os.getcwd()
path += "\\midiFiles\\"
path += f"{MIDI_FILE}.mid"

# Convert midi to wav file
fs.midi_to_audio(path, "output.wav")

# Open wav file and convert to mp3
song = AudioSegment.from_wav("output.wav")
song.export(f"{MIDI_FILE}.mp3", format="mp3")