from . import Animation
from the_sign import Sign
from the_sign.color import Color, Colors

try:
    from typing import Dict
except ImportError:
    pass


class Static(Animation):
    def __init__(self, img: Dict[int, Color], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = img

    def setup(self, sign: Sign):
        sign.fill(Colors.BLACK)
        for i, c in self.img.items():
            sign[i] = c
        sign.show()

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        pass


class SolidColor(Animation):
    def __init__(self, color: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    def setup(self, sign: Sign):
        sign.fill(self.color.with_brightness(self.max_brightness))
        sign.show()

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        pass
