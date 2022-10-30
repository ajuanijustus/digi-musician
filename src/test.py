from generateMIDI import generate_midi
from midiToMP3 import midi_to_mp3

# Define contant file name 
MIDI_FILENAME = "test_blues_minor"

base_note = 76 # int input?
scale_type = 'major' # drop down?
chords_flag = False #toggle
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 90   # In BPM
volume   = 100  

generate_midi(MIDI_FILENAME, base_note, scale_type = 'blues_minor', track = 0, channel = 0, time = 0, duration = 1, tempo = 120, volume = 100, chords_flag = True, chords_interval = 2, spook = False)
midi_to_mp3(MIDI_FILENAME)