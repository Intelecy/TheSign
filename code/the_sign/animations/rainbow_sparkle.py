import random

try:
    from typing import List, Dict
except ImportError:
    pass

from the_sign import Sign
from the_sign.animations import Animation
from the_sign.color import Colors


class RainbowSparkle(Animation):
    def __init__(
        self,
        max_sparks_per_second: int = 10,
        spark_duration_frames: int = 3,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.base_color = Colors.WHITE
        self.spark_duration_frames = spark_duration_frames
        self.when_spark: Dict[int, List[int]] = {}
        self.max_sparks_per_second = max_sparks_per_second
        self.sparks_per_period = int(self.max_sparks_per_second * self.duration)

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
                self.when_spark[f].append(
                    (random.randint(0, sign.n - 1), random.choice(Colors.COLORWHEEL))
                )

        sign.fill(self.base_color)

        for d in range(self.spark_duration_frames):
            f = frame_in_animation + d
            if f in self.when_spark:
                for dot, color in self.when_spark[f]:
                    sign[dot] = color
