import pygame.mixer

#사운드 생성
def firstsound():
    pygame.mixer.init()
    pygame.mixer.music.load("first.mp3")
    pygame.mixer.music.play()

def startsound():
    pygame.mixer.music.load("start.mp3")
    pygame.mixer.music.set_volume(0.50)
    pygame.mixer.music.play()

def effectsound():
    pygame.mixer.music.load("effect.mp3")
    pygame.mixer.music.play()


def endsound():
    pygame.mixer.music.load("end.mp3")
    pygame.mixer.music.play()