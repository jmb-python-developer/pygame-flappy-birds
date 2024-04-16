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

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

# Load sprite assets
assets.load_sprites()
# Load audio assets
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()


def create_sprites():
    # Draw them too, by instantiating, so then it scrolls to the left correctly constantly
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    # Bird Sprite
    return Bird(sprites), GameStartMessage(sprites), Score(sprites)


bird, game_started_message, score = create_sprites()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        # Capture event and trigger gamer start
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

    # Fill background with pink color (arbitrarily chosen)
    screen.fill(0)

    # Draw the screen object, from all the sprites pre-loaded into classes (see Background above for example)
    sprites.draw(screen)

    # if gamestarted message is removed and is not gameover for player, render/update all sprites in screen
    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
