from . import Animation
from the_sign import Sign
from the_sign.color import Color


class Blink(Animation):
    def __init__(self, color: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        if completed < 0.5:
            sign.fill(self.color)
        else:
            sign.clear()
