import pygame.sprite

import assets

# Sprite extending class for the background resource
import configs
from objects.layer import Layer


class Background(pygame.sprite.Sprite):
    # varargs groups
    def __init__(self, index, *groups):
        self._layer = Layer.BACKGROUND
        # Inherited image is the background asset
        self.image = assets.get_sprite("background")
        # Set into a rectangle
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH * index, 0))

        super().__init__(*groups)

    # Move the x coordinate by one to the left everytime method is called
    def update(self):
        self.rect.x -= 1

        if self.rect.right <= 0:
            self.rect.x = configs.SCREEN_WIDTH
