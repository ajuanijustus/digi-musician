# Import from modules
from generateMIDI import generate_midi
from midiToMP3 import midi_to_mp3

# Import modules
import pygame
import os
import sys
import shutil
import pretty_midi
import pandas as pd
import collections
import numpy as np

# Initialise the mixer module
pygame.mixer.init()
pygame.font.init()

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

class Note:
    def __init__(self, start, duration, note, note_length, song_length) -> None:
        self.start = start
        self.duration = duration
        self.note = note

        note_height = dict(zip("CDEFGAB",[0,1,2,3,4,5,6]))
        note_base_height = HEIGHT // 3 + 135
        chord_base_height = 2 * HEIGHT // 3 + 135

        gap_len = (WIDTH - 40) / (song_length // note_length)

        self.x = (self.start//note_length)*gap_len + 20

        if round(self.duration,2) == round(note_length,2):
            self.fill = False
            self.y = note_base_height
            # self.y -= (int(self.note[1])-4)*(7*15)
        else:
            self.fill = True
            self.y = chord_base_height

        self.y -= note_height[self.note[0]]*15
        
        self.note_h = 40
        self.radius = 8

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)

        if self.fill:
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius - 2)

        pygame.draw.line(screen, (0, 0, 0), (self.x+self.radius-1, self.y), (self.x+self.radius-1, self.y - self.note_h), 2)
        


# Function to generte new song
def gen_new(base_note, scale_type, chords_flag, tempo=90, spooky_mode=False, chords_interval = 2):
    # Stop the music so that the file is no longer open
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except:
        ...

    # Generate new set of notes
    generate_midi(MIDI_FILENAME, base_note, scale_type, chords_flag=chords_flag, tempo=tempo, spook=spooky_mode, chords_interval=chords_interval)
    midi_to_mp3(MIDI_FILENAME)

    # Load new midi file and start playing it
    mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")
    pygame.mixer.music.load(mp3_filename)

    raw_notes = midi_to_notes(midi_filename)
    get_note_names = np.vectorize(pretty_midi.note_number_to_name)
    sample_note_names = get_note_names(raw_notes['pitch'])

    starts = [i for i in np.vectorize(float)(raw_notes["start"])]
    ends = [i for i in np.vectorize(float)(raw_notes["end"])]
    durs = [i for i in np.vectorize(float)(raw_notes["duration"])]

    notes = list(zip(starts, durs, sample_note_names, ends))

    return notes


# Function to turn  midi_notes into a dataframe
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

def gen_notes(note_set):
    notes = []
    for note in note_set:
        notes.append(Note(*note[:3], min(note_set, key=lambda x: x[1])[1], max(note_set, key=lambda x: x[3])[3]))

    return notes

# Set screen width and height
WIDTH, HEIGHT = (800, 600)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define contant file name 
MIDI_FILENAME = "c_scale_withbass_random"

# Generating MIDI variables
base_note = 60
scale_type = 'major'
chords_flag = False
tempo = 90

# Get location of midi_file
path = os.getcwd()
midi_filename = os.path.join(path, "midiFiles", f"{MIDI_FILENAME}.mid")

# Generate midi files
p_notes = gen_new(base_note, scale_type, chords_flag)
notes = gen_notes(p_notes)

# Get mp3 filename
path = os.getcwd()
mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")

cat = pygame.image.load(os.path.join(path, "images", "catPump.jpg"))

# Load the song
pygame.mixer.music.load(mp3_filename)

# Create font to render
font = pygame.font.SysFont("Helvetica", 12)

# Dict to help flip text value
opp = {"Chords On":"Chords Off", "Chords Off":"Chords On"}
scale_opp = {
    "major":"natural minor", "natural minor":"blues minor",
    "blues minor":"blues major", "blues major":"major"
}

# Buttons
buttonGen = Button(10, 10, "Re-Generate")
buttonSave = Button(buttonGen.x+buttonGen.width+20, 10, "Save")
buttonChords = Button(buttonSave.x+buttonSave.width+20, 10, "Chords Off")
buttonScale = Button(buttonChords.x+buttonChords.width+20, 10, "major".title())

inputs = [
    IntInput(buttonScale.x+buttonScale.width+80, 10, "", 100),
    IntInput(buttonScale.x+buttonScale.width+200, 10, "", 100),
    IntInput(buttonSave.x+buttonSave.width+20, 50, "", 100)
]

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
    buttonScale.draw(screen)

    for input in inputs:
        input.draw(screen)

    # Check if first button hovered/clicked
    if buttonGen.hovered(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        if inputs[0].text != " ":
            base_note = int(inputs[0].text)
        if inputs[1].text != " ":
            tempo = int(inputs[1].text)
        if inputs[2].text != " ":
            chords_interval = int(inputs[2].text)
        
        p_notes = gen_new(base_note, scale_type, chords_flag, tempo=tempo, chords_interval=chords_interval)
        notes = gen_notes(p_notes)
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

    if buttonScale.hovered(*pygame.mouse.get_pos()) and mouse_pressed:
        buttonScale.text = scale_opp[buttonScale.text.lower()].title()
        buttonScale.rerender()
        scale = buttonScale.text.lower().replace(" ", "_")
    
    for input in inputs:
        if input.hovered(*pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                input.text=""
                input.typing = True
                input.inner_colour = 150
        elif pygame.mouse.get_pressed()[0]:
            input.typing = False
            input.inner_colour = 255
        
        if input.typing:
            for num in pressed_keys:
                if num == "back":
                    input.text = input.text[:-1]
                else:
                    input.text += num

                input.rerender()

    # Draw 4 lines
    for i in range(5):
        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT//3+30*i, WIDTH, 5))

    # Draw 4 lines
    for i in range(5):
        pygame.draw.rect(screen, (0, 0, 0), (0, 2*HEIGHT//3+30*i, WIDTH, 5))

    for note in notes:
        note.draw(screen)

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
            if inputs[0].text != " ":
                base_note = int(inputs[0].text)
            if inputs[1].text != " ":
                tempo = int(inputs[1].text)
            if inputs[2].text != " ":
                chords_interval = int(inputs[2].text)
            p_notes = gen_new(base_note, scale_type, chords_flag, tempo, True, chords_interval=chords_interval)
            notes = gen_notes(p_notes)
            spooky_mode = False
            play = False
        screen.blit(cat, (300, 10))
    
    # Update the screen
    pygame.display.flip()