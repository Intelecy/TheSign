try:
    from typing import List
except ImportError:
    pass

from . import Animation
from the_sign import Sign
from the_sign.color import Color, Colors


class RainbowCycle(Animation):
    def __init__(self, max_n: int = 37, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_n = max_n

        interval = 256 // max_n

        self.colors: List[Color] = [
            Colors.COLORWHEEL[i * interval].with_brightness(self.max_brightness)
            for i in range(max_n)
        ]

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        n = self.max_n

        for i in range(n):
            sign[i] = self.colors[i].mix(self.colors[(i + 1) % n], 1 - completed)

        if frame_in_animation == self.frame_count - 1:
            self.colors = [self.colors[-1]] + self.colors[:-1]
