import random

from the_sign.sequence import gen_rainbow

try:
    from typing import List, Dict
except ImportError:
    pass

from the_sign import Sign
from the_sign.animations import Animation, shuffle


class RainbowShimmer(Animation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rainbow = gen_rainbow(self.duration, self.frame_rate)
        self.rnd: List[int] = []
        self.step: int = 0

    def setup(self, sign: Sign):
        self.rnd = list(range(sign.n))
        shuffle(self.rnd)
        self.step = len(self.rainbow) // sign.n

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        for i in range(sign.n):
            sign[self.rnd[i]] = self.rainbow[
                (frame_in_animation + i * self.step) % len(self.rainbow)
            ]
