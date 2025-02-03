import random

try:
    from typing import List, Dict
except ImportError:
    pass

from the_sign import Sign
from the_sign.animations import Animation, bounce
from the_sign.color import Colors, Color


class Cube(Animation):
    edges = [15, 16, 17, 18, 24, 31, 33, 11, 7, 0]
    side_l = [36, 28, 27, 35, 29, 26, 34, 30, 25]
    side_r = [14, 4, 3, 13, 5, 2, 12, 6, 1]
    side_b = [32, 23, 19, 10, 8, 22, 20, 9, 21]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = [
            Colors.RED,
            Colors.GREEN,
            Colors.BLUE,
        ]

    def setup(self, sign: Sign):
        for i in self.edges:
            sign[i] = Colors.WHITE

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        c0 = self.colors[0].with_brightness(bounce(completed, True))
        c1 = self.colors[1].with_brightness(bounce(completed, True))
        c2 = self.colors[2].with_brightness(bounce(completed, True))

        for i in self.side_l:
            sign[i] = c0

        for i in self.side_r:
            sign[i] = c1

        for i in self.side_b:
            sign[i] = c2

        if frame_in_animation == self.frame_count - 1:
            self.colors = [self.colors[-1]] + self.colors[:-1]
