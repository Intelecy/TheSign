try:
    from typing import List, Dict
except ImportError:
    pass

from the_sign import Sign
from the_sign.animations import Animation
from the_sign.color import Colors


class Smile(Animation):
    _eye_left = [36, 28, 26, 25, 30, 35]
    _eye_right = [13, 4, 3, 2, 6, 12]
    _mouth = [33, 32, 22, 21, 9, 8, 0, 20]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, sign: Sign):
        sign.fill(Colors.YELLOW.with_brightness(0.3))

        for i in self._eye_left:
            sign[i] = Colors.GREEN.with_brightness(0.5)

        for i in self._eye_right:
            sign[i] = Colors.GREEN

        for i in self._mouth:
            sign[i] = Colors.BLUE

        sign[29] = Colors.RED
        sign[5] = Colors.RED
        sign[21] = Colors.PINK

        sign.show()

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        pass
