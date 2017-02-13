from random import random


class Snake:
    def __init__(self, window_dimensions):
        self.heading = (0, -1)
        # map just in case we ever go 3d..
        X1 = tuple(map(lambda x: x / 2, window_dimensions))
        X2 = tuple(map(lambda (x, dx): x + dx, zip(window_dimensions, self.heading)))
        self.tail = [X1, X2]
        self.window_dimensions = window_dimensions

    def eatApple(self, n):
        for _ in range(n):
            (x1, y1), (x2, y2) = self.tail[-2:]
            dx, dy = (x2 - x1, y2 - y1)
            new_tip = (x2 + dx, y2 + dy)
            self.tail.append(new_tip)

    def move(self):
        dx, dy = self.heading
        x, y = self.tail[:1][0]
        new_head = (x + dx, y + dy)
        if new_head in self.tail:
            raise Exception
        else:
            self.tail = [new_head] + self.tail[:-1]


class Apple:
    x = None
    y = None
    window_dimensions = None

    def __init__(self, window_dimensions, unavailable_pixels):
        self.window_dimensions = window_dimensions
        self.spawn(unavailable_pixels)

    def spawn(self, unavailable_pixels):
        x_dim, y_dim = self.window_dimensions
        self.x = int(random() * x_dim)
        self.y = int(random() * y_dim)

        while (self.x, self.y) in unavailable_pixels:
            self.x = int(random() * x_dim)
            self.y = int(random() * y_dim)
        return self.x, self.y


class SnakeGame:
    snake = None
    apple = None

    def __init__(self, window_dimensions):
        self.snake = Snake(window_dimensions)
        self.apple = Apple(window_dimensions, unavailable_pixels=self.snake.tail)

    def cheat_eat_apple(self):
        self.snake.eatApple(3)

    def move_snake(self):
        self.snake.move()
        if self.snake.tail[0] == (self.apple.x, self.apple.y):
            self.snake.eatApple(3)
            self.apple.spawn(self.snake.tail)

    def change_snake_heading(self, heading):
        self.snake.heading = heading

    def get_snake_tail(self):
        return self.snake.tail

    def get_apple_pos(self):
        return self.apple.x, self.apple.y
