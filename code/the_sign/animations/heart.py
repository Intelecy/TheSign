import random

try:
    from typing import List, Dict
except ImportError:
    pass

from the_sign import Sign
from the_sign.animations import Animation, bounce
from the_sign.color import Colors, Color


class Heart(Animation):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, sign: Sign):
        c = Colors.INTELECY
        sign.fill(c)

        for p in [27, 15, 14, 16, 33, 32, 22, 21, 9, 8, 0]:
            sign[p] = Colors.WHITE

        # sign[34] = c.mix(Colors.WHITE, 0.20)
        # sign[1] = c.mix(Colors.WHITE, 0.20)
        # sign[17] = c.mix(Colors.WHITE, 0.20)

        sign.show()

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        pass
