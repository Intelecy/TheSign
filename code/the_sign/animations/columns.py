from . import Animation
from the_sign import Sign
from the_sign.color import Colors


class Columns(Animation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, sign: Sign):
        sign.column(0, Colors.RED)
        sign.column(1, Colors.ORANGE)
        sign.column(2, Colors.YELLOW)
        sign.column(3, Colors.GREEN)
        sign.column(4, Colors.BLUE)
        sign.column(5, Colors.PURPLE)
        sign.column(6, Colors.WHITE)
        sign.show()

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        pass
