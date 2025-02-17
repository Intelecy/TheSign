import random

from . import Animation
from the_sign import Sign
from the_sign.color import Color
from ..sequence import gen_fade
from array import array

try:
    from typing import List, Optional
except ImportError:
    pass


class Shimmer(Animation):
    def __init__(self, c1: Color, c2: Color, speed: float = 1.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c1 = c1
        self.c2 = c2
        self.speed = speed

        self.fades: Optional[array] = None
        self.dot_map: Optional[List[int]] = None
        self.offsets: Optional[List[int]] = None

    def setup(self, sign: Sign):
        self.fades = []

        for d in [3, 4, 5, 6]:
            d /= self.speed
            self.fades.append(
                gen_fade(
                    self.c1,
                    self.c2,
                    d,
                    self.frame_rate,
                    bounce=True,
                )
            )

        self.dot_map = [0] * sign.n
        self.offsets = [0] * sign.n

        for i in range(sign.n):
            self.offsets[i] = random.randint(0, int(self.duration * self.frame_rate))

        self.reset(sign)

    def reset(self, sign: Sign):
        for i in range(sign.n):
            self.dot_map[i] = random.randint(0, len(self.fades) - 1)

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        # print(frame_in_animation)
        if frame_in_animation == 0:
            self.reset(sign)

        for i in range(sign.n):
            f = self.fades[self.dot_map[i]]
            o = self.offsets[i]
            sign[i] = f[(frame_in_animation + o) % len(f)]
