import random
import pygame.sprite

import assets
import configs
from objects.layer import Layer


class Column(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.gap = 100  # Set the vertical gap between the top and bottom pipes
        self._layer = Layer.OBSTACLE  # Assign the layer for obstacles

        # Load the pipe sprite
        self.sprite = assets.get_sprite("pipe-green")
        self.sprite_rect = self.sprite.get_rect()

        # Setup bottom pipe
        self.pipe_bottom = self.sprite
        self.pipe_bottom_rect = self.pipe_bottom.get_rect(
            topleft=(0, self.sprite_rect.height + self.gap))

        # Setup top pipe (flipped vertically)
        self.pipe_top = pygame.transform.flip(self.sprite, False, True)
        self.pipe_top_rect = self.pipe_top.get_rect(topleft=(0, 0))

        # Create an image surface to contain both the top and bottom pipe
        self.image = pygame.Surface(
            (self.sprite_rect.width, self.sprite_rect.height * 2 + self.gap),
            pygame.SRCALPHA)
        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)

        # Set position of the column (pipe pair)
        sprite_floor_height = assets.get_sprite("floor").get_rect().height
        min_y = 100
        max_y = configs.SCREEN_HEIGHT - sprite_floor_height - 100
        self.rect = self.image.get_rect(midleft=(configs.SCREEN_WIDTH, random.uniform(min_y, max_y)))
        self.mask = pygame.mask.from_surface(self.image)  # For collision detection

        self.passed = False  # Flag to check if the column has been passed by the bird

        super().__init__(*groups)  # Initialize the sprite with the given groups

    def update(self):
        """ Move the column leftwards; delete when out of the screen """
        self.rect.x -= 2  # Move column left by 2 pixels each frame

        # Remove the sprite when it moves out of the screen
        if self.rect.right <= 0:
            self.kill()

    def is_passed(self):
        """ Check if the bird has passed the column without hitting it """
        if self.rect.x < 50 and not self.passed:
            self.passed = True
            return True
        return False
