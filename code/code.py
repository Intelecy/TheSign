import gc
import time

import board
import asyncio
import adafruit_neopxl8
from the_sign import Sign
from the_sign.animations.knight_rider import KnightRider
from the_sign.animations.confetti import Confetti
from the_sign.animations.rainbow_shimmer import RainbowShimmer
from the_sign.animations.shimmer import Shimmer
from the_sign.animations.rainbow_cycle import RainbowRingCycle
from the_sign.animations.sparkle import Sparkle
from the_sign.animations.static import SolidColor
from the_sign.color import Colors
from micropython import const


NUM_PIXELS = const(37)
MS_PER_NS = const(1_000_000)
S_PER_NS = const(1_000 * MS_PER_NS)


class App:
    def __init__(self, frame_rate: int = 25, max_brightness: float = 1.0):
        self.start = None
        self.frame_rate = frame_rate
        self.max_brightness = max_brightness
        self.animation_length = 60

        self.pixels = adafruit_neopxl8.NeoPxl8(
            data0=board.NEOPIXEL0,
            n=NUM_PIXELS,
            num_strands=1,
            bpp=4,
            brightness=self.max_brightness,
            auto_write=False,
            pixel_order=adafruit_neopxl8.GRBW,
        )

        self.sign = Sign(self.pixels)
        self.sign.clear()

        self.current_animation = -1
        self.next_animation_at = 0

        # shimmer_intelecy = Shimmer(
        #     c1=Colors.INTELECY,
        #     c2=Colors.INTELECY.with_brightness(0.4),
        #     duration=self.animation_length,
        #     frame_rate=self.frame_rate,
        # )

        shimmer_intelecy = SolidColor(
            color=Colors.INTELECY,
            frame_rate=self.frame_rate,
        )

        shimmer_white = Shimmer(
            c1=Colors.WHITE,
            c2=Colors.WHITE.with_brightness(0.25),
            duration=self.animation_length,
            frame_rate=self.frame_rate,
        )

        self.animations = [
            shimmer_intelecy,
            Confetti(spark_duration_frames=10, frame_rate=self.frame_rate),
            shimmer_white,
            RainbowShimmer(
                duration=5,
                frame_rate=self.frame_rate,
            ),
            shimmer_intelecy,
            KnightRider(
                color=Colors.RED,
                duration=2,
                frame_rate=self.frame_rate,
            ),
            shimmer_white,
            RainbowRingCycle(duration=8, frame_rate=self.frame_rate),
            shimmer_intelecy,
            Sparkle(
                base_color=Colors.INTELECY,
                # flash_color=Colors.YELLOW,
                frame_rate=self.frame_rate,
            ),
            shimmer_white,
            Shimmer(
                c1=Colors.YELLOW,
                c2=Colors.RED,
                speed=3,
                duration=self.animation_length,
                frame_rate=self.frame_rate,
            ),
        ]

    async def draw_frame(self):
        now = time.monotonic()

        if now > self.next_animation_at:
            self.next_animation_at = now + self.animation_length
            self.current_animation = (self.current_animation + 1) % len(self.animations)
            self.animations[self.current_animation].setup(self.sign)

            gc.collect()

            total_memory = gc.mem_alloc() + gc.mem_free()
            free_memory = gc.mem_free()

            print(f"{self.current_animation}")
            print(f"Total memory: {total_memory} bytes")
            print(f"Free memory: {free_memory} bytes")
            print(f"Used memory: {gc.mem_alloc()} bytes")

            self.start = time.monotonic_ns()

        self.animations[self.current_animation].exec(self.sign, self.frame_number)
        self.sign.show()

    @property
    def elapsed(self) -> float:
        return (time.monotonic_ns() - self.start) / 1_000_000_000

    @property
    def frame_number(self) -> int:
        return int(self.frame_rate * self.elapsed)

    async def animate(self):
        await call_at_rate(self.frame_rate, self.draw_frame)

    # async def next_animation(self):
    #     print(f"next animation {self.current_animation}")
    #     self.current_animation = (self.current_animation + 1) % len(self.animations)
    #     self.animations[self.current_animation].setup(self.sign)

    async def run(self, run_for: float = 1.0):
        print("starting...")

        self.start = time.monotonic_ns()

        await asyncio.gather(
            call_at_rate("draw", self.frame_rate, self.draw_frame),
            # call_at_rate("next", 1 / 10, self.next_animation),
        )


async def call_at_rate(lbl: str, frame_rate: float, target_func, *args, **kwargs):
    """
    Call the target function at the specified framerate.

    Args:
        frame_rate (float): The desired frequency in Hz (e.g., 30 for 30 calls per second).
        target_func (coroutine): The async function to call.
        *args: Positional arguments to pass to the target function.
        **kwargs: Keyword arguments to pass to the target function.
    """
    interval = int(const(1000) // frame_rate)
    next_call_time = time.monotonic_ns() // MS_PER_NS

    while True:
        # print(f"{lbl} {time.monotonic_ns() // MS_PER_NS} calling target func...")
        await target_func(*args, **kwargs)
        # print(f"{lbl} {time.monotonic_ns() // MS_PER_NS} done calling target func")

        next_call_time += interval
        sleep_time = next_call_time - (time.monotonic_ns() // MS_PER_NS)

        if sleep_time < 0:
            print(
                f"{lbl} {time.monotonic_ns() // MS_PER_NS} target_func took too long to run. over={-1 * sleep_time} ms interval={interval}"
            )
            next_call_time = time.monotonic_ns() // MS_PER_NS
        # else:
        #     print(sleep_time)

        # print(f"{lbl} {time.monotonic_ns() // MS_PER_NS} sleeping for {sleep_time} ms")
        sleep_time = max(0, sleep_time)
        await asyncio.sleep_ms(sleep_time)


if board.board_id == "adafruit_feather_rp2040_scorpio":
    asyncio.run(App(frame_rate=2 * (1_000 // NUM_PIXELS)).run())
