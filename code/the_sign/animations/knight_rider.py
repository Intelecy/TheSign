from ..sequence import gen_fade, print_seq, new_buffer

try:
    from typing import List, Optional
except ImportError:
    pass

from . import Animation
from the_sign import Sign
from the_sign.color import Color, Colors


class KnightRider(Animation):
    def __init__(self, color=Colors.RED, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.grill: Optional[List[Color]] = None
        self.spacing: int = 8
        self.half: int = 0

    def setup(self, sign: Sign):
        d = self.duration
        self.grill = gen_fade(
            self.color,
            Colors.BLACK,
            d * 0.20,
            self.frame_rate,
        )
        self.grill.extend(new_buffer(d * 0.80, self.frame_rate))
        self.half = len(self.grill) // 2

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        if completed <= 0.5:
            for i in range(7):
                sign.column(
                    i,
                    self.grill[
                        (frame_in_animation - i * self.spacing) % len(self.grill)
                    ],
                )
        else:
            for i in reversed(range(7)):
                sign.column(
                    6 - i,
                    self.grill[
                        (frame_in_animation % self.half - i * self.spacing)
                        % len(self.grill)
                    ],
                )
