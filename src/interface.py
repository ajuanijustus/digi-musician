# Import from modules
from generateMIDI import generate_midi
from midiToMP3 import midi_to_mp3

# Import modules
import pygame
import os
import sys
import shutil
import pretty_midi

# Button Class
class Button:
    # Initialise function
    def __init__(self, x, y, text, border=5):
        self.x = x
        self.y = y
        self.text = text
        self.content = font.render(self.text, True, (0, 0, 0))
        self.width = self.content.get_width()
        self.height = self.content.get_height()
        self.border = border
        self.inner_colour = 255
    
    # Draw function
    def draw(self, screen):
        # Draw outer and inner rect
        pygame.draw.rect(screen, (0, 0, 0), (self.x-self.border, self.y-self.border, self.width + 2*self.border, self.height + 2*self.border))
        pygame.draw.rect(screen, [self.inner_colour]*3, (self.x, self.y, self.width, self.height))

        # Draw inner text
        screen.blit(self.content, (self.x, self.y))

    # Test if button hovered on
    def hovered(self, x, y):
        # Check if mouse within inner rect
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            # Show visually it is hovered on
            self.inner_colour = 150
            return True
        # Return to normal colour when not hovered on
        self.inner_colour = 255
        return False

    # Rerender text
    def rerender(self):
        # Redefine content, width and height
        self.content = font.render(self.text, True, (0, 0, 0))
        self.width = self.content.get_width()
        self.height = self.content.get_height()

# Input Class
class IntInput(Button):
    def __init__(self, x, y, text, width, border=5):
        super().__init__(x, y, text, border)
        self.width = width
        self.typing = False

    def rerender(self):
        saved_width = self.width
        super().rerender()
        if self.width > saved_width:
            self.text = self.text[:-1]
            self.rerender()
        
        self.width = saved_width
    
    def hovered(self, x, y):
        # Check if mouse within inner rect
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            # Show visually it is hovered on
            self.inner_colour = 150
            return True

        # Return to normal colour when not hovered on
        if not self.typing:
            self.inner_colour = 255
        return False

# Function to generte new song
def gen_new(base_note, scale_type, chords_flag, spooky_mode):
    # Stop the music so that the file is no longer open
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    # Generate new set of notes
    generate_midi(MIDI_FILENAME, base_note, scale_type, chords_flag, spooky_mode)
    midi_to_mp3(MIDI_FILENAME)

    # Load new midi file and start playing it
    mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")
    pygame.mixer.music.load(mp3_filename)

    print("done")

# Define contant file name 
MIDI_FILENAME = "c_scale_withbass_random"

# Generating MIDI variables
base_note = 60
scale_type = 'major'
chords_flag = False

# Generate midi files
generate_midi(MIDI_FILENAME, base_note, scale_type, chords_flag)
midi_to_mp3(MIDI_FILENAME)

# Code to get notes
import pretty_midi
import pandas as pd
import collections
import numpy as np
from matplotlib import pyplot as plt
import matplotlib

matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import pylab


path = os.getcwd()
midi_filename = os.path.join(path, "midiFiles", f"{MIDI_FILENAME}.mid")

def midi_to_notes(midi_file: str) -> pd.DataFrame:
  pm = pretty_midi.PrettyMIDI(midi_file)
  instrument = pm.instruments[0]
  notes = collections.defaultdict(list)

  # Sort the notes by start time
  sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
  prev_start = sorted_notes[0].start

  for note in sorted_notes:
    start = note.start
    end = note.end
    notes['pitch'].append(note.pitch)
    notes['start'].append(start)
    notes['end'].append(end)
    notes['step'].append(start - prev_start)
    notes['duration'].append(end - start)
    prev_start = start

  return pd.DataFrame({name: np.array(value) for name, value in notes.items()})

raw_notes = midi_to_notes(midi_filename)
get_note_names = np.vectorize(pretty_midi.note_number_to_name)
sample_note_names = get_note_names(raw_notes['pitch'])
print(sample_note_names[:10])

def plot_piano_roll(notes: pd.DataFrame):
    title = f'Whole track'
    count = len(notes['pitch'])
    # plt.figure(figsize=(20, 4))
    fig = pylab.figure(figsize=(20, 4), # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
    plot_pitch = np.stack([notes['pitch'], notes['pitch']], axis=0)
    plot_start_stop = np.stack([notes['start'], notes['end']], axis=0)
    # plt.plot(plot_start_stop[:, :count], plot_pitch[:, :count], color="b", marker=".")
    # plt.xlabel('Time [s]')
    # plt.ylabel('Pitch')
    # _ = plt.title(title)
    ax = fig.gca()
    ax.plot(plot_start_stop[:, :count], plot_pitch[:, :count], color="b", marker=".")
    return fig, ax

fig, ax = plot_piano_roll(raw_notes)
canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()
size = canvas.get_width_height()

# screen = pygame.display.get_surface()
# surf = pygame.image.fromstring(raw_data, size, "RGB")
# screen.blit(surf, (0,0))
# pygame.display.flip()

# crashed = False
# while not crashed:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             crashed = True

# Get mp3 filename
path = os.getcwd()
mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")

# Initialise the mixer module
pygame.mixer.init()
pygame.font.init()

cat = pygame.image.load(os.path.join(path, "images", "catPump.jpg"))

# Load the song
pygame.mixer.music.load(mp3_filename)

# Create font to render
font = pygame.font.SysFont("Helvetica", 12)

# Set screen width and height
WIDTH, HEIGHT = (800, 600)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Dict to help flip text value
opp = {"Chords On":"Chords Off", "Chords Off":"Chords On"}

# Buttons
buttonGen = Button(10, 10, "Re-Generate")
buttonChords = Button(80, 10, "Chords Off")
buttonSave = Button(260, 10, "Save")
intInput = IntInput(140, 10, " ", 100)

# Var to keep track of music
play = False
spooky_keys = [pygame.K_s, pygame.K_p, pygame.K_k, pygame.K_y]
spooky_mode = False

# Main interface loop
while True:
    pressed_keys = []
    k = pygame.key.get_pressed()
    spooky = [k[i] for i in spooky_keys]
    mouse_pressed = False

    # Manage each event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.unicode in list("1234567890"):
                pressed_keys.append(event.unicode)
            elif event.key == pygame.K_BACKSPACE:
                pressed_keys.append("back")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True


    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw buttons
    buttonGen.draw(screen)
    buttonChords.draw(screen)
    buttonSave.draw(screen)
    intInput.draw(screen)

    # Check if first button hovered/clicked
    if buttonGen.hovered(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        if intInput.text != " ":
            base_note = int(intInput.text)
        gen_new(base_note, "major", chords_flag, False)
        play = False

    # Check if second button hovered/clicked
    if buttonChords.hovered(*pygame.mouse.get_pos()) and mouse_pressed:
        buttonChords.text = opp[buttonChords.text]
        buttonChords.rerender()
        chords_flag = not chords_flag

    if buttonSave.hovered(*pygame.mouse.get_pos()) and mouse_pressed:
        mp3_path = os.path.join(path, "mp3Files")
        files = os.listdir(mp3_path)
        shutil.copy(mp3_filename, os.path.join(mp3_path, f"song{len(files)-1}.mp3"))
        
    if intInput.hovered(*pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            intInput.typing = True
            intInput.inner_colour = 150
    elif pygame.mouse.get_pressed()[0]:
        intInput.typing = False
        intInput.inner_colour = 255
    
    if intInput.typing:
        for num in pressed_keys:
            if num == "back":
                intInput.text = intInput.text[:-1]
            else:
                intInput.text += num

            intInput.rerender()

    # Draw 4 lines
    screen = pygame.display.get_surface()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0,0))
    pygame.display.flip()
    # for i in range(5):
    #     pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT//2+30*i, WIDTH, 5))

    # If not already playing, play the notes
    if not play:
        pygame.mixer.music.play()
        play = True

    if sum(spooky) == 4:
        spooky_mode = True
    
    if spooky_mode:
        cat_x = 293+cat.get_width()//2
        cat_y = 18+cat.get_height()//2
        cat_wid = 15
        cat_hight = 8
        mx, my = pygame.mouse.get_pos()
        if cat_x <= mx <= cat_x+cat_wid and cat_y <= my <= cat_y+cat_hight and mouse_pressed:
            if intInput.text != " ":
                base_note = int(intInput.text)
            gen_new(base_note, scale_type, chords_flag, True)
            spooky_mode = False
            play = False
        screen.blit(cat, (300, 10))
    
    # Update the screen
    pygame.display.flip()