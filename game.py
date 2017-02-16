from random import random


class RanIntoBody(Exception):
    pass

class RanIntoWall(Exception):
    pass

class Snake:
    def __init__(self, window_dimensions):
        self.heading = (0, -1)
        # map just in case we ever go 3d..
        X1 = tuple(map(lambda x: x / 2, window_dimensions))
        X2 = tuple(map(lambda (x, dx): x + dx, zip(window_dimensions, self.heading)))
        self.tail = [X1, X2]
        self.window_dimensions = window_dimensions

    def _snake_in_bounds(self, new_head):
        nhx, nhy = new_head
        wind_x, wind_y = self.window_dimensions
        return (0 <= nhx <= wind_x) and (0 <= nhy <= wind_y)

    def eatApple(self, n):
        for _ in range(n):
            (x1, y1), (x2, y2) = self.tail[-2:]
            dx, dy = (x2 - x1, y2 - y1)
            new_tip = (x2 + dx, y2 + dy)
            self.tail.append(new_tip)

    def move(self):
        dx, dy = self.heading
        x, y = self.tail[0] #head
        new_head = (x + dx, y + dy)
        #nhx, nhy = new_head
        if (new_head in self.tail):
            #print 'ran into itself', (new_head in self.tail)

            raise RanIntoBody
        elif not(self._snake_in_bounds(new_head)):
            raise RanIntoWall
        else:
            self.tail = [new_head] + self.tail[:-1]

    def get_head(self):
        return self.tail[0]

    def get_dist_to_nearest_border(self):
        pass

class Apple:
    x = None
    y = None
    window_dimensions = None

    def __init__(self, window_dimensions, unavailable_pixels):
        self.window_dimensions = window_dimensions
        # self.spawn(unavailable_pixels)
        self.x = window_dimensions[0] / 2
        self.y = window_dimensions[1] / 3

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
        """

        :return: whether or not it got this reward
        """
        self.snake.move()
        if self.snake.tail[0] == (self.apple.x, self.apple.y):
            self.snake.eatApple(3)
            self.apple.spawn(self.snake.tail)
            return True
        return False

    def change_snake_heading(self, heading):
        self.snake.heading = heading

    def get_snake_tail(self):
        return self.snake.tail

    def get_apple_pos(self):
        return self.apple.x, self.apple.y
