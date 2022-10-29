from platform import platform
import pygame
import os
import sys

path = os.getcwd()
FILE_NAME = "major-scale"

pygame.mixer.init()

pygame.mixer.music.load(path+f"\\mp3Files\\{FILE_NAME}.mp3")

WIDTH, HEIGHT = (800, 600)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

play = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((255, 255, 255))

    for i in range(4):
        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT//2+30*i, WIDTH, 5))


    if not play:
        pygame.mixer.music.play()
        play = True
    
    pygame.display.flip()