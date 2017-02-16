from game import SnakeGame
import pygame
import random
from collections import defaultdict
import sys


"""
0: UP
1: DOWN
2: LEFT
3: RIGHT
"""

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

window_dimensions = (300, 300)
pixel_mult = 6
SCREEN = None
CLOCK = None
GAME = None

snake_color = (0, 250, 0)
apple_color = (250, 0, 0)

add_tuple = lambda pos1, pos2 : (pos1[0] + pos2[0], pos1[1] + pos2[1])

random.seed(42)

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
    CLOCK.tick(30)

def step(action):
    pygame.event.get()
    GAME.change_snake_heading(DIRECTIONS[action])
    done = False
    has_reward = False
    try:
        has_reward = GAME.move_snake()
        render()
    except Exception as e:
        print type(e)
        done = True

    return (GAME.get_apple_pos(), GAME.snake.get_head(), GAME.snake.heading), has_reward, done

def get_available_actions():
    """
    prevent snake from turning back on itself
    :return:
    """
    head = GAME.snake.tail[0]
    head_plus_1 = GAME.snake.tail[1]
    actions = []
    for i in range(len(DIRECTIONS)):
        dir = DIRECTIONS[i]
        if add_tuple(dir, head) != head_plus_1:
            actions.append(i)
    return sorted( actions )

def senses_surroundings():
    """
    Need to finish this... method.
    :return:
    """
    snake_head = GAME.snake.get_head()
    tail_set = set(GAME.snake.tail)
    sense = []
    for possible_headings in get_available_actions():
        one_step_look_ahead = add_tuple(snake_head, DIRECTIONS[possible_headings])
        sense.append(one_step_look_ahead in tail_set)
    return tuple(sense)


def find_best_move(apple_pos, snake_pos, heading):
    min_manhattan_dist = float('inf')
    best_action = 0 #default best action to prevent none being returned
    snake_x, snake_y = snake_pos
    for action in get_available_actions():
        dx, dy = DIRECTIONS[action]
        if  (snake_x + dx, snake_y + dy) not in GAME.snake.tail:
            dist = manhattan_dist(apple_pos, (snake_x + dx, snake_y + dy))
            if dist < min_manhattan_dist:
                min_manhattan_dist = dist
                best_action = action
    return best_action

class QLearning:

    def __init__(self, num_actions):
        self.table = defaultdict(lambda : [random.random()/10.0 for _ in range(4)]) #keys are states and values are q values for each action
        #self.table = defaultdict(lambda: [0.0 for _ in range(4)])  # keys are states and values are q values for each action

        self.eps = 0.2
        self.gamma = 0.97
        self.step_penalty = 0.1
        self.learning_rate = 0.25

    def update(self, state, action, reward, state_prime):
        if reward < -25:
            print 'YOU DIED!!!!', state, action, DIRECTIONS[action]
        #TODO: if somethings wrong look at the default dict
        maxQ = max(self.table[state_prime]) #max q-value from subsequent state
        currentQ = self.table[state][action]
        self.table[state][action] += self.learning_rate * ((reward - self.step_penalty) + (self.gamma * maxQ) - currentQ)

    def predict(self, state):
        #choose the best move that doesnt kill the snake
        q_vals = self.table[state]
        av_actions = get_available_actions()
        return sorted([(act, q_vals[act]) for act in av_actions] , key = lambda x: x[1], reverse = True)[0]





if __name__ == "__main__":

    ACTION_SPACE_SIZE = len(DIRECTIONS)

    qlearn = QLearning(num_actions=ACTION_SPACE_SIZE)

    #func to calculate state tuple as diff in position

    manhattan_dist = lambda pos1, pos2 : abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    #_get_state = manhattan_dist
    def _get_state(apple_pos, snake_pos, heading):
        dist_range = min(5, manhattan_dist(apple_pos, snake_pos))
        dx = apple_pos[0] - snake_pos[0]
        dy = apple_pos[1] - snake_pos[1]
        max_mag = 1 #table space = max_mag * max_mag * NUM_ACTIONS
        if dx < 0:
            dx = - min(abs(dx), max_mag)
        else:
            dx = min(abs(dx), max_mag)

        if dy < 0:
            dy = - min(abs(dy), max_mag)
        else:
            dy = min(abs(dy), max_mag)
        hx, hy = heading
        return (dx, dy, hx, hy, senses_surroundings())
        #return (dx, dy, senses_surroundings())



    n_episodes = 500.0
    for epoch in range(1000):
        state = init_env()
        #eps = 1.0 / (epoch + 1.0)
        #eps = 0.9**(epoch + 1)
        if epoch < 25.0:
            eps = 0.9
        else:
            eps = 0.2
        #eps = (n_episodes - epoch)/ (n_episodes+ 1.0)
        print epoch, 'Epsilon', eps
        total_reward = 0.0
        total_steps = 0.0
        while True:
            method = None
            prior_tail = GAME.snake.tail
            av_actions = get_available_actions()
            action = av_actions[0]
            if random.random() < eps:
                if random.random() < 0.6:
                    method = 'best move'
                    action = find_best_move(*state)
                    _, value = qlearn.predict(_get_state(*state)) #check learning
                    method = 'best move %s'%str(qlearn.table[_get_state(*state)])
                else:
                    action, value = qlearn.predict(_get_state(*state))
                    method = 'qlearning %s' % str(qlearn.table[_get_state(*state)])

                    # action = random.choice(get_available_actions())
                    # method = 'random action %s' % str(qlearn.table[_get_state(*state)])
            else:
                action, value = qlearn.predict(_get_state(*state))
                method = 'qlearning %s'%str(qlearn.table[_get_state(*state)])

            is_done = False
            if action is None:
                print 'Action None dumping available actions', get_available_actions(), qlearn.predict(_get_state(*state)), _get_state(*state)
            state_prime, reward, is_done = step(action)

            reward_val = 0.0
            if is_done:
                reward_val = -20.0
            elif reward:
                reward_val = 100.0
            elif state_prime[2] != state[2]: #heading changed penalty
                reward_val = -1.0

            qlearn.update(_get_state(*state), action, reward_val, _get_state(*state_prime))
            gs, gs_p = _get_state(*state), _get_state( *state_prime )
            if gs != gs_p:
                print 'diff', total_steps, gs, reward, action, gs_p , is_done,  method, eps, reward_val

            state = state_prime

            total_reward += reward_val
            total_steps += 1.0
            if is_done  or total_steps > 500:
                print 'prior_tail', prior_tail, av_actions
                print 'action', DIRECTIONS[action], method

                print 'tail', GAME.snake.tail
                print 'Game Finished'
                break
        print epoch, 'reward steps', total_reward, total_steps
        #for k,v in qlearn.table.items():
        #    print 'state: ', k, 'qvalues: ', [round(x, 2) for x in v]
    print 'Size of Q Learning Table', len(qlearn.table)