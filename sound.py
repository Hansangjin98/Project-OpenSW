import pygame.mixer

#사운드 생성
def startsound():
    pygame.mixer.init()
    pygame.mixer.music.load("start.mp3")
    pygame.mixer.music.play()

def effectsound():
    pygame.mixer.music.load("effect.mp3")
    pygame.mixer.music.play()

def sound_pause():
    pygame.mixer.pause()
def sound_unpause():
    pygame.mixer.unpause()

def endsound():
    pygame.mixer.music.load("end.mp3")
    pygame.mixer.music.play()