from ..sequence import gen_rainbow

try:
    from typing import List, Optional
except ImportError:
    pass

from . import Animation
from the_sign import Sign
from the_sign.color import Color, Colors


class RainbowRingCycle(Animation):
    def __init__(self, max_n: int = 37, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grad: Optional[List[Color]] = []
        self.step = 48

    def setup(self, sign: Sign):
        self.grad = gen_rainbow(self.duration, self.frame_rate)

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        for i in range(4):
            sign.ring(
                3 - i,
                self.grad[(frame_in_animation + i * self.step) % len(self.grad)],
            )
