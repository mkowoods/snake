from game import SnakeGame
import pygame
import random
from collections import defaultdict

"""
0: UP
1: DOWN
2: LEFT
3: RIGHT
"""

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

window_dimensions = (500, 500)
pixel_mult = 6
SCREEN = None
CLOCK = None
GAME = None

snake_color = (0, 250, 0)
apple_color = (250, 0, 0)

def init_env():
    pygame.init()
    global SCREEN, CLOCK, GAME
    SCREEN = pygame.display.set_mode(window_dimensions)
    CLOCK = pygame.time.Clock()
    GAME = SnakeGame((window_dimensions[0] / pixel_mult, window_dimensions[1] / pixel_mult))
    return (GAME.get_apple_pos(), GAME.snake.get_head(), GAME.snake.heading)

def render():
    SCREEN.fill((0, 0, 0))

    x, y = GAME.get_apple_pos()
    pygame.draw.rect(SCREEN, apple_color, pygame.Rect(x * pixel_mult, y * pixel_mult, pixel_mult, pixel_mult))

    tail = GAME.get_snake_tail()
    for x, y in tail:
        pygame.draw.rect(SCREEN, snake_color, pygame.Rect(x * pixel_mult, y * pixel_mult, pixel_mult, pixel_mult))

    pygame.display.flip()
    CLOCK.tick(10)

def step(action):
    pygame.event.get()
    GAME.change_snake_heading(DIRECTIONS[action])
    done = False
    has_reward = False
    try:
        has_reward = GAME.move_snake()
        render()
    except:
        done = True
    return (GAME.get_apple_pos(), GAME.snake.get_head(), GAME.snake.heading), has_reward, done


class QLearning:

    def __init__(self, num_actions):
        self.table = defaultdict(lambda : [0.0, 0.0, 0.0, 0.0]) #keys are states and values are q values for each action
        self.eps = 0.2
        self.gamma = 0.97
        self.step_penalty = 0.1
        self.learning_rate = 0.95

    def update(self, state, action, reward, state_prime):
        #TODO: if somethings wrong look at the default dict
        maxQ = max(self.table[state_prime]) #max q-value from subsequent state
        currentQ = self.table[state][action]
        self.table[state][action] += self.learning_rate * ((reward - self.step_penalty) + (self.gamma * maxQ) - currentQ)

    def predict(self, state):
        #choose the best move that doesnt kill the snake
        q_vals = self.table[state]
        return sorted(enumerate(q_vals), key = lambda x: x[1], reverse = True)[0]





if __name__ == "__main__":

    ACTION_SPACE_SIZE = len(DIRECTIONS)

    qlearn = QLearning(num_actions=ACTION_SPACE_SIZE)

    #func to calculate state tuple as diff in position

    manhattan_dist = lambda apple_pos, snake_pos, _ : abs(apple_pos[0] - snake_pos[0]) + abs(apple_pos[1] - snake_pos[1])
    #_get_state = manhattan_dist
    def _get_state(apple_pos, snake_pos, _):
        dx = apple_pos[0] - snake_pos[0]
        dy = apple_pos[1] - snake_pos[1]
        if dx < 0:
            dx = - min(abs(dx), 20)
        else:
            dx = min(abs(dx), 20)

        if dy < 0:
            dy = - min(abs(dy), 20)
        else:
            dy = min(abs(dy), 20)
        return (dx, dy)


    def find_best_move(apple_pos, snake_pos, heading):
        min_manhattan_dist = float('inf')
        best_action = None
        snake_x, snake_y = snake_pos
        for action, dir in enumerate(DIRECTIONS):
            dx, dy = dir
            if  (snake_x + dx, snake_y + dy) not in GAME.snake.tail:
                dist = manhattan_dist(apple_pos, (snake_x + dx, snake_y + dy), None)
                if dist < min_manhattan_dist:
                    min_manhattan_dist = dist
                    best_action = action
        return best_action




    for epoch in range(20):
        state = init_env()
        #eps = 1.0 / (epoch + 1.0)
        eps = 0.95**(epoch + 1)
        print 'Epsilon', eps
        total_reward = 0.0
        total_steps = 0.0
        while True:
            method = None
            if random.random() < eps:
                if random.random() < 1.0:
                    method = 'best_move'
                    action = find_best_move(*state)
                    _, value = qlearn.predict(_get_state(*state)) #check learning
                    method = 'best_move %s'%str(qlearn.table[_get_state(*state)])
                else:
                    method = 'random action'
                    action = random.randint(0, 3)
                    #action = qlearn.predict(_get_state(*state))
            else:
                action, value = qlearn.predict(_get_state(*state))
                method = 'qlearning %s'%str(qlearn.table[_get_state(*state)])

            state_prime, reward, is_done = step(action)
            print _get_state( *state), reward, action, _get_state( *state_prime ), is_done, method, eps

            reward_val = 0.0
            if is_done:
                reward_val = -20.0
            elif reward:
                reward_val = 100.0

            qlearn.update(_get_state(*state), action, reward_val, _get_state(*state_prime))

            state = state_prime

            total_reward += reward_val
            total_steps += 1.0
            if is_done:
                print 'Game Finished'
                break
        print epoch, 'reward steps', total_reward, total_steps
    print qlearn.table