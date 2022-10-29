from generateMIDI import *
from midiToMP3 import *

# Define contant file name 
MIDI_FILENAME = "c_scale_withbass_random"

base_note = 60
scale_type = 'major'
chords_flag = False

generate_midi(MIDI_FILENAME, base_note, scale_type, chords_flag)
midi_to_mp3(MIDI_FILENAME)