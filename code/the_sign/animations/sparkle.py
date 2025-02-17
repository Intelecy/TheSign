import random

try:
    from typing import List, Dict
except ImportError:
    pass

from the_sign import Sign
from the_sign.animations import Animation
from the_sign.color import Colors, Color


class Sparkle(Animation):
    def __init__(
        self,
        base_color: Color,
        flash_color: Color = Colors.WHITE,
        max_sparks_per_second: int = 4,
        spark_duration_frames: int = 5,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.base_color = base_color
        self.flash_color = flash_color
        self.spark_duration_frames = spark_duration_frames
        self.when_spark: Dict[int, List[int]] = {}
        self.max_sparks_per_second = max_sparks_per_second
        self.sparks_per_period = int(self.max_sparks_per_second * self.duration)
        step_sz = 0.333 / self.spark_duration_frames
        self.blended = [
            # self.flash_color.with_brightness(1 - i * step_sz)
            self.flash_color.mix(self.base_color, i * step_sz)
            for i in range(self.spark_duration_frames)
        ]

    def setup(self, sign: Sign):
        sign.fill(self.base_color)
        sign.show()

    def render(self, sign: Sign, frame_in_animation: int, completed: float):
        if frame_in_animation == 0:
            self.when_spark = {}
            for _ in range(self.sparks_per_period):
                f = random.randint(0, self.frame_count)
                if f not in self.when_spark:
                    self.when_spark[f] = []
                self.when_spark[f].append(random.randint(0, sign.n - 1))

        sign.fill(self.base_color)

        for d in range(self.spark_duration_frames):
            f = frame_in_animation + d
            if f in self.when_spark:
                for dot in self.when_spark[f]:
                    sign[dot] = self.blended[d]
