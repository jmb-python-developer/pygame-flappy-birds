import pygame
import assets
import configs

from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

# Initialize the pygame module
pygame.init()

# Set up the display with dimensions from config
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

# Load game assets
assets.load_sprites()
assets.load_audios()

# Create a layered update group for all sprites
sprites = pygame.sprite.LayeredUpdates()


def create_sprites():
    """ Create initial set of sprites for the game and handle their layering. """
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    # Return initialized bird, start message, and score objects
    return Bird(sprites), GameStartMessage(sprites), Score(sprites)


# Initialize game components
bird, game_started_message, score = create_sprites()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
                game_started_message.kill()
                pygame.time.set_timer(column_create_event, 1500)
            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted = False
                sprites.empty()
                bird, game_started_message, score = create_sprites()

        if not gameover:
            bird.handle_event(event)

    # Clear screen to a single color (can be modified)
    screen.fill(0)

    # Draw all sprites on the screen
    sprites.draw(screen)

    if gamestarted and not gameover:
        # Update all sprites
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")

    # Update score and play point sound if a column is passed
    for sprite in sprites:
        if isinstance(sprite, Column) and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    # Refresh game screen
    pygame.display.flip()
    clock.tick(configs.FPS)

# Quit pygame when the main loop is exited
pygame.quit()
