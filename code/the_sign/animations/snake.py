import random
from collections import deque

try:
    from typing import Iterable
except ImportError:
    pass

from the_sign import Sign
from the_sign.animations import Animation
from the_sign.color import Colors, Color

#          15
#       27    14
#    28    16    04
# 36    26    13    03
#    29    17    05
# 35    25    12    02
#    30    18    06
# 34    24    11    01
#    31    19    07
# 33    23    10    00
#    32    20    08
#       22    09
#          21

# axes: [ /, \ ]
# centered on 18
# positive values move down
coords = [
    [0,3], # 0
    [-1,2], # 1
    [-2,1], # 2
    [-3,0], # 3
    [-3,-1], # 4
    [-2,0], # 5
    [-1,1], # 6
    [0,2], # 7
    [1,3], # 8
    [2,3], # 9
    [1,2], # 10
    [0,1], # 11
    [-1,0], # 12
    [-2,-1], # 13
    [-3,-2], # 14
    [-3,-3], # 15
    [-2,-2], # 16
    [-1,-1], # 17
    [0,0], # 18
    [1,1], # 19
    [2,2], # 20
    [3,3], # 21
    [3,2], # 22
    [2,1], # 23
    [1,0], # 24
    [0,-1], # 25
    [-1,-2], # 26
    [-2,-3], # 27
    [-1,-3], # 28
    [0,-2], # 29
    [1,-1], # 30
    [2,0], # 31
    [3,1], # 32
    [3,0], # 33
    [2,-1], # 34
    [1,-2], # 35
    [0,-3], # 36
]

def dist(a: int, b: int) -> int:
    ac = coords[a]
    bc = coords[b]
    dx = ac[0] - bc[0]
    dy = ac[1] - bc[1]
    if (dx > 0 and dy < 0) or (dx < 0 and dy > 0) :
        return abs(dx) + abs(dy)
    else:
        return max(abs(dx), abs(dy))

neighbors_list = [
    [1, 7, 8],
    [0, 2, 6, 7],
    [1, 3, 5, 6],
    [2, 4, 5],
    [3, 5, 13, 14],
    [2, 3, 4, 6, 12, 13],
    [1, 2, 5, 7, 11, 12],
    [0, 1, 6, 8, 10, 11],
    [0, 7, 9, 10],
    [8, 10, 20, 21],
    [7, 8, 9, 11, 19, 20],
    [6, 7, 10, 12, 18, 19],
    [5, 6, 11, 13, 17, 18],
    [4, 5, 12, 14, 16, 17],
    [4, 13, 15, 16],
    [14, 16, 27],
    [13, 14, 15, 17, 26, 27],
    [12, 13, 16, 18, 25, 26],
    [11, 12, 17, 19, 24, 25],
    [10, 11, 18, 20, 23, 24],
    [9, 10, 19, 21, 22, 23],
    [9, 20, 22],
    [20, 21, 23, 32],
    [19, 20, 22, 24, 31, 32],
    [18, 19, 23, 25, 30, 31],
    [17, 18, 24, 26, 29, 30],
    [16, 17, 25, 27, 28, 29],
    [15, 16, 26, 28],
    [26, 27, 29, 36],
    [25, 26, 28, 30, 35, 36],
    [24, 25, 29, 31, 34, 35],
    [23, 24, 30, 32, 33, 34],
    [22, 23, 31, 33],
    [31, 32, 34],
    [30, 31, 33, 35],
    [29, 30, 34, 36],
    [28, 29, 35],
]

# Generate colors:
length = 7
head = Colors.PINK
tail = Colors.YELLOW
colors = []
for i in range(0,length+1):
    colors.append(head.mix(tail, float(i)/float(length)))
print(colors)
snake_colors = [
    Color(r=0, g=0, b=255, w=0),  # blue
    Color(r=29, g=0, b=226, w=0),
    Color(r=60, g=0, b=195, w=0),
    Color(r=89, g=0, b=166, w=0),
    Color(r=120, g=0, b=135, w=0),
    Color(r=149, g=0, b=106, w=0),
    Color(r=180, g=0, b=75, w=0),
    Color(r=210, g=0, b=45, w=0),  # pink
    Color(r=203, g=13, b=38, w=0),
    Color(r=196, g=27, b=32, w=0),
    Color(r=189, g=41, b=25, w=0),
    Color(r=181, g=54, b=19, w=0),
    Color(r=174, g=68, b=13, w=0),
    Color(r=167, g=82, b=6, w=0),
    Color(r=159, g=96, b=0, w=0),  # yellow
]


def neighbors(i: int) -> list[int]:
    if 0 <= i < len(neighbors_list):
        return neighbors_list[i]
    raise Exception("Unknown index")


def free(possible: Iterable[int], occupied: Iterable[int]) -> list[int]:
    p = set(possible)
    o = set(occupied)
    return list(p.difference(o))


def make_snake(length: int):
    head = random.randint(0, 36)
    snake = [head]
    while len(snake) < length:
        tail = snake[-1]
        f = free(neighbors(tail), snake)

        # if we fail to find any free neighbors, just return
        if len(f) == 0:
            return snake

        snake.append(random.choice(f))
    return snake


class State:
    def __init__(self):
        self.alive = True
        self.prize = 0
        self.snake = deque([])
        self.reset()

    def reset(self):
        self.alive = True
        self.snake = deque(make_snake(4), 37)
        self.prize = random.choice(free(range(0, 37), self.snake))

    def closest_to_prize(self, options: list[int]) -> list[int]:
        min_dist = 100
        closest = []

        for x in options:
            d = dist(x, self.prize)
            if d < min_dist:
                min_dist = d
                closest = [x]
            elif d == min_dist:
                closest.append(x)

        return closest


    def update(self):
        if self.alive:
            self.update_alive()
        else:
            if len(self.snake) == 1:
                self.reset()
            else:
                self.snake.pop()

    def update_alive(self):
        head = self.snake[0]
        f = free(neighbors(head), self.snake)
        if len(f) == 0:
            self.alive = False
            return

        next_free = random.choice(self.closest_to_prize(f))

        if next_free == self.prize:
            self.snake.appendleft(next_free)
            self.prize = random.choice(free(range(0, 37), self.snake))
        else:
            self.snake.appendleft(next_free)
            self.snake.pop()


class Snake(Animation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # n updates per second
        self.frames_per_alive_update = self.frame_rate // 4
        self.frames_per_dead_update = self.frames_per_alive_update // 4

        self.base_color = Colors.BLACK
        self.prize_color = Colors.INTELECY

        self.snake_colors = snake_colors
        self.dead_snake_color = Colors.RED

        self.state = State()

    def setup(self, sign: Sign):
        self.state.reset()

    def frames_per_update(self):
        if self.state.alive:
            return self.frames_per_alive_update
        else:
            return self.frames_per_dead_update

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        if frame_in_animation % self.frames_per_update() != 0:
            return

        self.state.update()

        sign.fill(self.base_color)

        if self.state.alive:
            for i, idx in enumerate(self.state.snake):
                if i < len(self.snake_colors):
                    sign[idx] = self.snake_colors[i]
                else:
                    sign[idx] = self.snake_colors[-1]
        else:
            for idx in self.state.snake:
                sign[idx] = self.dead_snake_color

        sign[self.state.prize] = self.prize_color
