from generateMIDI import *
from midiToMP3 import *

# Define contant file name 
MIDI_FILENAME = "major-scale"

generate_midi(MIDI_FILENAME)
midi_to_mp3(MIDI_FILENAME)