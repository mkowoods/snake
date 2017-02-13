from game import SnakeGame

import pygame

window_dimensions = (400, 300)

pygame.init()
screen = pygame.display.set_mode(window_dimensions)
done = False

clock = pygame.time.Clock()

snake_color = (0, 250, 0)
apple_color = (250, 0, 0)

game = SnakeGame(window_dimensions)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_q]:
        done = True

    if pressed[pygame.K_x]:
        game.cheat_eat_apple()

    heading = None
    if pressed[pygame.K_UP]:
        heading = (0, -1)
    if pressed[pygame.K_DOWN]:
        heading = (0, 1)
    if pressed[pygame.K_LEFT]:
        heading = (-1, 0)
    if pressed[pygame.K_RIGHT]:
        heading = (1, 0)
    if heading:
        game.change_snake_heading(heading)

    try:
        game.move_snake()
    except:
        done = True

    screen.fill((0, 0, 0))

    x, y = game.get_apple_pos()
    pygame.draw.rect(screen, apple_color, pygame.Rect(x, y, 1, 1))

    for x, y in game.get_snake_tail():
        pygame.draw.rect(screen, snake_color, pygame.Rect(x, y, 1, 1))

    pygame.display.flip()
    # clock.tick(30)
