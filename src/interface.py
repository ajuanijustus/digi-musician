# Import from modules
from generateMIDI import generate_midi
from midiToMP3 import midi_to_mp3

# Import modules
import pygame
import os
import sys
import pretty_midi

# Define contant file name 
MIDI_FILENAME = "major-scale"

path = os.getcwd()
midi_filename = os.path.join(path, "midiFiles", f"{MIDI_FILENAME}.mid")

pm = pretty_midi.PrettyMIDI(midi_filename)

for inst in pm.instruments:
    print(inst.notes)

# Get mp3 filename
path = os.getcwd()
mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")

# Initialise the mixer module
pygame.mixer.init()
pygame.font.init()

# Load the song
pygame.mixer.music.load(mp3_filename)

font = pygame.font.SysFont("Helvetica", 12)
text = font.render("Re-Generate", True, (0, 0, 0))

# Set screen width and height
WIDTH, HEIGHT = (800, 600)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Button border
BORDER = 5
BUTTON_X = 10
BUTTON_Y = 10
BUTTON_WIDTH = text.get_width() + BORDER
BUTTON_HEIGHT = text.get_height() + BORDER

inner_colour = 255

# Main interface loop
play = False
while True:
    # Manage each event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Clear the screen
    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0, 0, 0), (BUTTON_X - BORDER, BUTTON_Y - BORDER, BUTTON_WIDTH+2*BORDER, BUTTON_HEIGHT+2*BORDER))
    pygame.draw.rect(screen, [inner_colour]*3, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))

    m_x, m_y = pygame.mouse.get_pos()

    if BUTTON_X < m_x < BUTTON_X + BUTTON_WIDTH and BUTTON_Y < m_y < BUTTON_Y + BUTTON_HEIGHT:
        inner_colour = 150
        if pygame.mouse.get_pressed()[0]:
            # Generate new set of notes
            generate_midi(MIDI_FILENAME)
            midi_to_mp3(MIDI_FILENAME)

            # Load new midi file and start playing it
            mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")
            pygame.mixer.music.load(mp3_filename)

            play = False
    else:
        inner_colour = 255

    screen.blit(text, (BUTTON_X, BUTTON_Y))

    # Draw 4 lines
    for i in range(5):
        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT//2+30*i, WIDTH, 5))

    # If not already playing, play the notes
    if not play:
        pygame.mixer.music.play()
        play = True
    
    # Update the screen
    pygame.display.flip()