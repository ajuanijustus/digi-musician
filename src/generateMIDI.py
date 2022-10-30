import os
import random
from midiutil import MIDIFile

'''
Major chord: 0 +4 +3
Minor chord : 0 +3 +4
Diminished chord: 0 +3 +3

MIDI note numbers
.60 - C4 (middle C)
.24 - C1
.36 - C2
.48 - C3

Bass assumption: Base note for bass chord is melody note -36 (3 octaves).
'''

base_note_options = range(60, 96) # C4 to C7
scale_type_options = ['major', 'natural_minor', 'harmonic_minor', 'melodic_minor']

def generate_scale(base_note=60, scale_type='major'):
    i = base_note
    if scale_type == 'major':
        scale  = [i, i+2, i+4, i+5, i+7, i+9, i+11, i+12]  # T T S T T T S
    elif scale_type == 'natural_minor':
        scale  = [i, i+2, i+3, i+5, i+7, i+8, i+10, i+12] # T S T T S T T
    elif scale_type == 'harmonic_minor':
        scale  = [] #T – S – T – T – S – T1⁄2 – S
    elif scale_type == 'melodic_minor':
        scale  = [] #acs. T – S – T – T – T – T – S and on desc T – T – S – T – T – S – T
    else:
        print('Invalid scale_type. scale_type defaulting to "major"')
        scale  = [i, i+2, i+4, i+5, i+7, i+9, i+11, i+12]
    return scale

def generate_midi(MIDI_FILENAME, base_note, scale_type, track = 0,
channel = 0, time = 0, duration = 1, tempo = 90, volume = 100,
chords_flag=False, spook = False):
    volume_diff_for_chords = 10
    scale = generate_scale(base_note, scale_type)

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
    MyMIDI.addTempo(track, time, tempo)

    if spook == True:
        scale = [base_note, base_note+3, base_note+6, base_note+9, base_note+12, base_note+15, base_note+18]
        for i, pitch in enumerate([random.choice(scale) for x in range(20)]):
            # melody
            MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
            # bass chord - minus 36 for bass chord's base
            if (i%4 == 0) and chords_flag:
                MyMIDI.addNote(track, channel, pitch-36, time + i, 3, volume-volume_diff_for_chords)
                MyMIDI.addNote(track, channel, pitch-36+3, time + i, 3, volume-volume_diff_for_chords)
                MyMIDI.addNote(track, channel, pitch-36+6, time + i, 3, volume-volume_diff_for_chords)
    else:
        for t in range(20):
            i = random.choice(range(len(scale)))
            pitch = scale[i]
            # melody
            MyMIDI.addNote(track, channel, pitch, time + t, duration, volume)
            # bass chord: minus 36 (3 octaves) for bass chord's base
            if (t%4 == 0) and chords_flag:
                if i in [0, 3, 4, 7]: # major chords
                    MyMIDI.addNote(track, channel, pitch-36, time + t, 3, volume-volume_diff_for_chords)
                    MyMIDI.addNote(track, channel, pitch-36+4, time + t, 3, volume-volume_diff_for_chords)
                    MyMIDI.addNote(track, channel, pitch-36+7, time + t, 3, volume-volume_diff_for_chords)
                elif i in [1, 2, 5]: # minor chords
                    MyMIDI.addNote(track, channel, pitch-36, time + t, 3, volume-volume_diff_for_chords)
                    MyMIDI.addNote(track, channel, pitch-36+3, time + t, 3, volume-volume_diff_for_chords)
                    MyMIDI.addNote(track, channel, pitch-36+7, time + t, 3, volume-volume_diff_for_chords)
                else: # diminished chords
                    MyMIDI.addNote(track, channel, pitch-36, time + t, 3, volume-volume_diff_for_chords)
                    MyMIDI.addNote(track, channel, pitch-36+3, time + t, 3, volume-volume_diff_for_chords)
                    MyMIDI.addNote(track, channel, pitch-36+6, time + t, 3, volume-volume_diff_for_chords)

    path = os.getcwd()
    with open(path+"/midiFiles/" + MIDI_FILENAME + ".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)