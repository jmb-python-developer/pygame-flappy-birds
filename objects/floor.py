import pygame.sprite

import assets
import configs
from objects.layer import Layer


class Floor(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        # Assign the layer for floor elements
        self._layer = Layer.FLOOR
        self.image = assets.get_sprite("floor")  # Load the floor sprite
        # Set the initial position of the floor based on its index
        self.rect = self.image.get_rect(bottomleft=(configs.SCREEN_WIDTH * index, configs.SCREEN_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for collision purposes
        super().__init__(*groups)  # Initialize the sprite with the given groups

    def update(self):
        """ Move the floor sprite horizontally to create a scrolling effect. """
        self.rect.x -= 2  # Move the floor to the left by 2 pixels

        # If the floor completely moves out of the screen, reset its position to the right
        if self.rect.right <= 0:
            self.rect.x = configs.SCREEN_WIDTH
