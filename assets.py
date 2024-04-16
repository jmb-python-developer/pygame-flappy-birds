import os
import pygame

# Maps for loaded assets with their ids as filenames
sprites = {}
audios = {}


# Load game sprites into a map
def load_sprites():
    path = os.path.join("assets", "sprites")
    for file in os.listdir(path):
        # Keep the filename only [0], not extension [1]
        sprites[file.split(".")[0]] = pygame.image.load(os.path.join(path, file))


# Provide sprite from map, key is string for the filename part (see above)
def get_sprite(name):
    return sprites[name]


def load_audios():
    path = os.path.join("assets", "audios")
    for file in os.listdir(path):
        # Keep the filename only [0], not extension [1]
        audios[file.split(".")[0]] = pygame.mixer.Sound(os.path.join(path, file))


def play_audio(name):
    audios[name].play()
