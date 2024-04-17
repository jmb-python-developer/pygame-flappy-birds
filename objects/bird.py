import pygame.sprite

import assets
import configs
from objects.column import Column
from objects.floor import Floor
from objects.layer import Layer


class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.PLAYER  # Assign the layer for player
        # Load different sprites for animation
        self.images = [
            assets.get_sprite("redbird-midflap"),
            assets.get_sprite("redbird-downflap"),
            assets.get_sprite("redbird-upflap"),
        ]
        self.image = self.images[0]  # Start with the midflap image
        self.rect = self.image.get_rect(topleft=(-50, 50))  # Initial position of the bird
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for collision detection
        self.flap = 0  # Initial flap value
        super().__init__(*groups)  # Initialize the sprite with the given groups

    def update(self):
        """ Cycle through images to create a flapping animation, manage gravity. """
        # Rotate through the bird images to create an animation effect
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]
        # Gravity effect: increase the 'flap' value to simulate falling
        self.flap += configs.GRAVITY
        self.rect.y += self.flap  # Apply the gravity to the bird's vertical position

        # If the bird reaches the screen bottom, it moves slightly up
        if self.rect.x < 50:
            self.rect.x += 3

    def handle_event(self, event):
        """ Handle events like space key press to make the bird flap. """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.flap = 0  # Reset the flap value
            self.flap -= 6  # Move the bird up
            assets.play_audio("wing")  # Play wing flap sound

    def check_collision(self, sprites):
        """ Check for collisions with columns or the floor, or if bird goes too high. """
        for sprite in sprites:
            if (isinstance(sprite, Column) or isinstance(sprite, Floor)) and (
                    sprite.mask.overlap(self.mask, (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y))
                    or self.rect.bottom < 0):  # Check if bird hits the top of the screen
                return True
        return False
