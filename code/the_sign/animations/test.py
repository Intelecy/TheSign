try:
    from typing import List, Optional
except ImportError:
    pass

from . import Animation
from the_sign import Sign
from the_sign.color import Color, Colors
from ..sequence import gen_rainbow


class TestAnimation(Animation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rainbow: Optional[List[Color]] = None
        self.spacing: int = 1
        self.border = Colors.WHITE.with_brightness(0.2)

    def setup(self, sign: Sign):
        self.rainbow = gen_rainbow(self.duration, self.frame_rate)
        self.spacing = len(self.rainbow) // 20
        sign.fill(self.border)

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        sign.number(3, Colors.RED)

        # t = len(self.rainbow)
        # for i in range(7):
        #     sign.column(
        #         i,
        #         self.rainbow[(frame_in_animation + i * self.spacing) % t],
        #     )
        #
        # sign.ring3 = self.border
