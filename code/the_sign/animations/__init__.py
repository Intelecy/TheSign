try:
    import typing

    if typing.TYPE_CHECKING:
        from the_sign.sign import Sign
except ImportError:
    pass


class Animation:
    def __init__(
        self,
        frame_rate: int,
        duration: float = 1.0,
        offset: float = 0,
        max_brightness: float = 1.0,
    ):
        """
        This class initializes the parameters necessary for handling a sequence of
        frames, defining their rate, duration, starting offset, and brightness level.
        It is used to calculate the total number of frames based on the provided
        frame rate and duration.

        :param frame_rate: The number of frames displayed per second.
        :type frame_rate: int
        :param duration: The total length of time in seconds for which frames
            are displayed. Defaults to 1.0.
        :type duration: float
        :param offset: The initial offset in seconds before the frame sequence
            starts. Defaults to 0.
        :type offset: float
        :param max_brightness: The maximum brightness level for the sequence of
            frames. Defaults to 1.0.
        :type max_brightness: float
        """
        self.duration = duration
        self.frame_rate = frame_rate
        self.offset = offset
        self.max_brightness = max_brightness

        self.frame_count = int(self.duration * self.frame_rate)

    def exec(self, sign: "Sign", frame_number: int):
        frame_number += self.offset * self.frame_rate
        frame_in_animation = frame_number % self.frame_count

        self.render(
            sign,
            frame_in_animation,
            float(frame_in_animation) / float(self.frame_count),
        )

    def setup(self, sign: "Sign"):
        pass

    def render(self, sign: "Sign", frame_in_animation: int, completed: float):
        pass


class NOP(Animation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def bounce(completed: float, inverse: bool = False) -> float:
    if completed < 0.5:
        r = 1 - completed * 2
    else:
        r = (completed - 1) * 2 + 1

    if inverse:
        return 1 - r

    return r
