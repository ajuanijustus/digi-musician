# Import libraries
import os

# Import from libraries
from midi2audio import FluidSynth
from pydub import AudioSegment

# Instantiate fluid synth
fs = FluidSynth()

def midi_to_mp3(MIDI_FILENAME):

    # Gen path to file
    path = os.getcwd()
    midi_filename = os.path.join(path, "midiFiles", f"{MIDI_FILENAME}.mid")
    mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")
    wav_filename = os.path.join(path, "tempFiles", "output.wav")

    # Convert midi to wav file
    fs.midi_to_audio(midi_filename, wav_filename)

    # Open wav file and convert to mp3
    song = AudioSegment.from_wav(wav_filename)
    song.export(mp3_filename, format="mp3")