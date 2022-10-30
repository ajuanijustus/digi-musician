from generateMIDI import generate_midi
from midiToMP3 import midi_to_mp3

# Define contant file name 
MIDI_FILENAME = "c_scale_withbass_random"

base_note = 60 # int input?
scale_type = 'major' # drop down?
chords_flag = False #toggle

generate_midi(MIDI_FILENAME, base_note, scale_type, chords_flag, spook = True)
midi_to_mp3(MIDI_FILENAME)