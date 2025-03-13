from .shimmer import Shimmer
from the_sign import Sign
from the_sign.color import Color, Colors


class InnovationNorge(Shimmer):
    logo = [4, 5, 6, 7, 8, 10, 19, 24, 32]

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, c1=Colors.WHITE, c2=Colors.WHITE.with_brightness(0.25), **kwargs
        )

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        super().render(sign, frame_in_animation, completed)

        for p in self.logo:
            sign[p] = Colors.RED
