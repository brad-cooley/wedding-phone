import pygame
import time

pygame.mixer.init()
sound = pygame.mixer.Sound('mysound.wav')
playing = sound.play()

for i in range(5):
    playing.queue(sound)


while playing.get_busy():
    pass

print(playing.get_queue())