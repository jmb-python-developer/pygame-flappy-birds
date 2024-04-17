import pygame.sprite

import assets
import configs
from objects.layer import Layer


class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        # Assign the layer for UI elements
        self._layer = Layer.UI
        self.value = 0  # Initialize score value to 0
        # Create a transparent surface for score display
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
        # Position the score at the center top of the screen
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))
        self.__create()  # Call the method to update the score display
        super().__init__(*groups)  # Initialize the sprite

    def __create(self):
        """ Create the score display by converting the score value to images of digits. """
        self.str_value = str(self.value)
        self.images = []
        self.width = 0

        # Loop over each character in the score's string representation
        for str_value_char in self.str_value:
            img = assets.get_sprite(str_value_char)  # Get the sprite for each digit
            self.images.append(img)  # Append the digit image to the list
            self.width += img.get_width()  # Increment total width by digit's width

        # Height is the height of the first digit image
        self.height = self.images[0].get_height() if self.images else 0
        # Re-create the surface based on total width and height of score
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, 50))

        # Blit each digit image onto the score surface at the correct position
        x = 0
        for img in self.images:
            self.image.blit(img, (x, 0))
            x += img.get_width()

    def update(self):
        """ Update the score display whenever the score changes. """
        self.__create()
