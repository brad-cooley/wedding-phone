import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound('sound.wav')
playing = sound.play()

while playing.get_busy():
    pygame.time.delay(100)
    print('playing sound')