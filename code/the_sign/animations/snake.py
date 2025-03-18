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

snake_colors = [
    Color(r=0, g=0, b=255, w=0),  # blue
    Color(r=42, g=0, b=214, w=0),
    Color(r=84, g=0, b=172, w=0),
    Color(r=126, g=0, b=130, w=0),
    Color(r=168, g=0, b=88, w=0),
    Color(r=210, g=0, b=45, w=0),  # pink
    Color(r=200, g=19, b=36, w=0),
    Color(r=190, g=38, b=27, w=0),
    Color(r=180, g=57, b=18, w=0),
    Color(r=170, g=76, b=9, w=0),
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
        self.prize = None
        self.snake = None
        self.reset()

    def reset(self):
        self.snake = deque(make_snake(6), 37)
        self.prize = random.choice(free(range(0, 37), self.snake))

    def update(self):
        head = self.snake[0]
        f = free(neighbors(head), self.snake)
        if len(f) == 0:
            # oh no! we ran into ourselves. For now just reset
            self.reset()
            return

        next_free = random.choice(f)

        if next == self.prize:
            self.prize = random.choice(free(range(0, 37), self.snake))
            self.snake.appendleft(next_free)
        else:
            self.snake.appendleft(next_free)
            self.snake.pop()


class Snake(Animation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # n updates per second
        self.frames_per_update = self.frame_rate // 4

        self.base_color = Colors.BLACK
        self.prize_color = Colors.INTELECY

        self.snake_head_color = Colors.PINK
        self.snake_tail_color = Colors.YELLOW

        self.snake_colors = snake_colors
        # max_length = 5
        # for i in range(0,max_length+1):
        #     self.snake_colors.append(self.snake_head_color.mix(self.snake_tail_color, float(i)/float(max_length)))

        self.state = None

    def setup(self, sign: Sign):
        self.state = State()

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        if frame_in_animation % self.frames_per_update != 0:
            return

        self.state.update()

        sign.fill(self.base_color)

        for i, idx in enumerate(self.state.snake):
            if i < len(self.snake_colors):
                sign[idx] = self.snake_colors[i]
            else:
                sign[idx] = self.snake_tail_color

        sign[self.state.prize] = self.prize_color
