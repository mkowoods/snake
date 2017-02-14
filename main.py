from game import SnakeGame
import pygame

window_dimensions = (500, 500)
pixel_mult = 6

pygame.init()
screen = pygame.display.set_mode(window_dimensions)
done = False

clock = pygame.time.Clock()

snake_color = (0, 250, 0)
apple_color = (250, 0, 0)


game = SnakeGame((window_dimensions[0] / pixel_mult, window_dimensions[1] / pixel_mult))

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
    elif pressed[pygame.K_DOWN]:
        heading = (0, 1)
    elif pressed[pygame.K_LEFT]:
        heading = (-1, 0)
    elif pressed[pygame.K_RIGHT]:
        heading = (1, 0)
    
    # remember first boolean evaluates first because of 'and'
    if heading and game.snake.heading == (heading[0] * -1, heading[1]*-1):
        pass
    elif heading:
        game.change_snake_heading(heading)

    try:
        game.move_snake()
    except:
        done = True

    screen.fill((0, 0, 0))

    x, y = game.get_apple_pos()
    pygame.draw.rect(screen, apple_color, pygame.Rect(x*pixel_mult, y*pixel_mult, pixel_mult, pixel_mult))

    tail = game.get_snake_tail()
    for x, y in tail:
        pygame.draw.rect(screen, snake_color, pygame.Rect(x*pixel_mult, y*pixel_mult, pixel_mult, pixel_mult))

    pygame.display.flip()
    clock.tick(10)
