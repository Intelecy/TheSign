import time
import board
import asyncio
import adafruit_neopxl8
from the_sign import Sign
from the_sign.animations.cube import Cube
from the_sign.animations.rainbow_cycle import RainbowCycle
from the_sign.animations.rainbow_sparkle import RainbowSparkle
from the_sign.animations.shimmer import Shimmer
from the_sign.animations.sparkle import Sparkle
from the_sign.color import Colors
from micropython import const


NUM_PIXELS = const(37)
MS_PER_NS = const(1_000_000)


class App:
    def __init__(self, frame_rate: int = 25, max_brightness: float = 1.0):
        self.start = time.monotonic_ns()
        self.frame_rate = frame_rate
        self.max_brightness = max_brightness

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

        self.current_animation = 0

        self.animations = [
            # RainbowSparkle(frame_rate=self.frame_rate),
            # Cube(duration=2.5, frame_rate=self.frame_rate),
            # Shimmer(
            #     c1=Colors.INTELECY,
            #     c2=Colors.INTELECY.with_brightness(0.5),
            #     duration=5,
            #     frame_rate=self.frame_rate,
            # ),
            # RainbowCycle(duration=0.2, frame_rate=self.frame_rate),
            Sparkle(
                base_color=Colors.INTELECY,
                # flash_color=Colors.INTELECY,
                frame_rate=self.frame_rate,
            ),
        ]

        self.animations[self.current_animation].setup(self.sign)

    async def draw_frame(self):
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

    async def next_animation(self):
        self.current_animation = (self.current_animation + 1) % len(self.animations)

    async def run(self, run_for: float = 1.0):
        print("starting...")
        t1 = asyncio.create_task(self.animate())
        # t2 = asyncio.create_task(call_at_rate(1 / 10, self.next_animation))

        await asyncio.gather(t1)


async def call_at_rate(frame_rate: float, target_func, *args, **kwargs):
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
        await target_func(*args, **kwargs)

        next_call_time += interval
        sleep_time = next_call_time - (time.monotonic_ns() // MS_PER_NS)

        if sleep_time < 0:
            print(f"target_func took too long to run. over={-1 * sleep_time} ms")
            next_call_time = time.monotonic_ns() // MS_PER_NS
        # else:
        #     print(sleep_time)

        await asyncio.sleep_ms(max(0, sleep_time))


if board.board_id == "adafruit_feather_rp2040_scorpio":
    asyncio.run(App(frame_rate=30, max_brightness=1.0).run())
