from typing import List

from the_sign import Sign
from the_sign.animations import Animation
from the_sign.color import Colors, Color


class RainbowSpin(Animation):
    def __init__(self, clockwise: bool = True, steps: int = 32, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clockwise = clockwise
        self.steps = steps

        interval = 256 // steps

        self.colors: List[Color] = [
            Colors.COLORWHEEL[i * interval].with_brightness(self.max_brightness)
            for i in range(steps)
        ]

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        for i, px in enumerate(sign.ring3):
            sign[px] = self.colors[i].mix(
                self.colors[(i + 1) % len(sign.ring3)], 1 - completed
            )
