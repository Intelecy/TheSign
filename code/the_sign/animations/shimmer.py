import random

from . import Animation, bounce
from the_sign import Sign
from the_sign.color import Color


class Shimmer(Animation):
    def __init__(self, c1: Color, c2: Color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c1 = c1
        self.c2 = c2
        self.duration_scale = []
        self.offsets = []
        self.next_duration_scale = []
        self.next_offsets = []

    def setup(self, sign: Sign):
        sign.fill(self.c1)
        sign.show()

        # Initialize current and next values for smooth transitions
        self.duration_scale = [random.uniform(0.8, 1) for _ in range(sign.n)]
        self.offsets = [random.uniform(0.5, 1) for _ in range(sign.n)]
        self.next_duration_scale = self.duration_scale[:]
        self.next_offsets = self.offsets[:]

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        # Initiate new target values at the start of animation cycle
        if frame_in_animation == 0:
            self.next_duration_scale = [random.uniform(0.8, 1) for _ in range(sign.n)]
            self.next_offsets = [random.uniform(0.5, 1) for _ in range(sign.n)]

        # Interpolate between current and next values for smoother transitions
        interpolation_factor = completed  # Progress through the animation cycle
        current_duration_scale = [
            self._lerp(
                self.duration_scale[i],
                self.next_duration_scale[i],
                interpolation_factor,
            )
            for i in range(sign.n)
        ]
        current_offsets = [
            self._lerp(self.offsets[i], self.next_offsets[i], interpolation_factor)
            for i in range(sign.n)
        ]

        # Apply brightness and update LEDs
        for i in range(sign.n):
            b = completed * current_duration_scale[i] + current_offsets[i]
            b %= 1
            sign[i] = self.c1.with_brightness(self._lerp(bounce(b), 1.0, 0.5))

        # Update the current values at the end of the cycle
        if frame_in_animation == self.frame_count - 1:
            self.duration_scale = self.next_duration_scale[:]
            self.offsets = self.next_offsets[:]

    @staticmethod
    def _lerp(start: float, end: float, factor: float) -> float:
        """
        Linearly interpolates between two values.
        :param start: Starting value.
        :param end: Target value.
        :param factor: Interpolation factor (0.0 to 1.0).
        :return: Interpolated value.
        """
        return start + (end - start) * factor
