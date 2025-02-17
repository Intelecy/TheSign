import time
import board
from micropython import const
from math import floor

adapt_colors = board.board_id != "GENERIC_LINUX_PC"

GAMMA = const(1.7)

try:
    from typing import Optional, Tuple, Union, Sequence, List

    ColorUnion = Union[int, Tuple[int, int, int], Tuple[int, int, int, int]]
except ImportError:
    pass


def colorwheel(n: float) -> int:
    """Generate a 24-bit RGB color from a color wheel.

    Args:
        n (float): Position in the color wheel (0-255, floats are truncated).

    Returns:
        int: 24-bit integer color (0xRRGGBB).
    """
    # n = int(n) % 256  # Ensure it's within 0-255
    n %= 256

    if n < 85:
        r, g, b = 255 - n * 3, n * 3, 0
    elif n < 170:
        n -= 85
        r, g, b = 0, 255 - n * 3, n * 3
    else:
        n -= 170
        r, g, b = n * 3, 0, 255 - n * 3

    return (int(r) << 16) | (int(g) << 8) | int(b)  # Pack into 0xRRGGBB format


class Color:
    __slots__ = "values"

    _GAMMA_TABLE = [round((i / 255) ** GAMMA * 255) for i in range(256)]

    def __init__(self, r: int, g: int, b: int, w: int = 0):
        self.values = [r, g, b, w]

    def pack(self, gamma: bool = False) -> int:
        if gamma:
            return self.with_gamma().pack()  # TODO(jonathan)
        return (self.w << 24) | (self.r << 16) | (self.g << 8) | self.b

    @staticmethod
    def from_packed(packed: int) -> "Color":
        """
        Create a Color instance from a packed 32-bit integer.
        :param packed: 32-bit integer where:
                       bits 24-31 = w, bits 16-23 = r, bits 8-15 = g, bits 0-7 = b
        """
        w = (packed >> 24) & 0xFF
        r = (packed >> 16) & 0xFF
        g = (packed >> 8) & 0xFF
        b = packed & 0xFF

        return Color(r, g, b, w)

    @property
    def r(self):
        return self.values[0]

    @r.setter
    def r(self, value):
        self.values[0] = value

    @property
    def g(self):
        return self.values[1]

    @g.setter
    def g(self, value):
        self.values[1] = value

    @property
    def b(self):
        return self.values[2]

    @b.setter
    def b(self, value):
        self.values[2] = value

    @property
    def w(self):
        return self.values[3]

    @w.setter
    def w(self, value):
        self.values[3] = value

    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b}, w={self.w})"

    def with_brightness(self, brightness: float) -> "Color":
        """
        Return a new Color instance with adjusted brightness.
        Brightness is an integer from 0 (off) to 255 (full brightness).
        """
        if brightness == 1.0:
            return Color(*self.values)

        if not 0.0 <= brightness <= 1.0:
            raise ValueError("Brightness must be between 0.0 and 1.0.")

        # Scale all color components by brightness using integer math
        scale = (
            round(brightness * 256) + 1
        )  # Avoid losing precision with integer division
        values = [(component * scale) // 256 for component in self.values]
        return Color(*values)

    def gamma(self) -> list[int, int, int, int]:
        """
        Apply gamma correction using a lookup table and return the gamma-corrected values.
        """
        return [Color._GAMMA_TABLE[component] for component in self.values]

    def with_gamma(self) -> "Color":
        return Color(*self.gamma())

    def mix(self, color: "Color", weight: float = 0.5) -> "Color":
        """
        Blend this color with another color using the specified weight.
        Weight is a float between 0.0 and 1.0:
          - 0.0 = this color only
          - 1.0 = other color only
        """

        if weight <= 0.0:
            return self

        if weight >= 1.0:
            return color

        # Convert weight to an integer in the range 0–256 for integer math
        weight_scaled = floor(weight * 256)
        inv_weight_scaled = 256 - weight_scaled

        # Compute the blended components
        blended_values = [
            (self.values[i] * inv_weight_scaled + color.values[i] * weight_scaled)
            // 0xFF
            for i in range(4)
        ]

        return Color(*blended_values)


class Colors:
    BLACK = Color(0, 0, 0)
    WHITE = Color(0, 0, 0, 255)

    if adapt_colors:
        RED = Color(255, 0, 0)
        ORANGE = Color.from_packed(colorwheel(12))
        YELLOW = Color.from_packed(colorwheel(32))
        GREEN = Color(0, 255, 0)
        BLUE = Color(0, 0, 255)
        PURPLE = Color.from_packed(colorwheel(200))
        PINK = Color.from_packed(colorwheel(240))
        # INTELECY = Color(0, 255, 40)
        INTELECY = Color(28, 255, 81)
    else:
        RED = Color(255, 0, 0)
        ORANGE = Color.from_packed(colorwheel(42.5))
        YELLOW = Color(255, 255, 0)
        GREEN = Color(0, 255, 0)
        BLUE = Color(0, 0, 255)
        PURPLE = Color.from_packed(colorwheel(165))
        PINK = Color.from_packed(colorwheel(195))
        INTELECY = Color(0, 255, 40)

    COLORWHEEL = [Color.from_packed(colorwheel(i)) for i in range(256)]


def benchmark(fn, *args, label: str = "func", c: int = 1_000, **kwargs):
    start = time.monotonic_ns()
    for _ in range(c):
        fn(*args, **kwargs)
    stop = time.monotonic_ns()

    ns = int((stop - start) / c)

    print(f"{label}: {ns:.2f} ns per call ({1 / (ns / 1_000_000):.2f} per ms)")


def run_test():
    import board
    import adafruit_neopxl8
    from adafruit_neopxl8 import NeoPxl8
    import adafruit_fancyled.adafruit_fancyled as fancy

    print("hello")

    pixels = NeoPxl8(
        data0=board.NEOPIXEL0,
        n=1,
        num_strands=1,
        bpp=4,
        brightness=1,
        auto_write=False,
        pixel_order=adafruit_neopxl8.GRBW,
    )

    pixels.fill((0, 0, 0))
    pixels[0] = (0, 0, 255)
    pixels.show()

    color = Color(255, 0, 0)

    def set_pixel():
        pixels[0] = (255, 0, 0)

    benchmark(set_pixel)

    # def set_pixel():
    #     pixels[0] = tuple(WHITE)
    #
    # benchmark(set_pixel)

    # def set_pixel():
    #     pixels[0] = WHITE.as_tuple()
    #
    # benchmark(set_pixel)

    def set_pixel():
        pixels[0] = color.values

    benchmark(set_pixel)

    pixels.show()

    print(Colors.RED)
    print(Colors.RED.with_brightness(0.5))
    print(Colors.RED.pack(True))

    f1 = fancy.CRGB(200, 0, 0)
    # print(f"f1.pack  {f1.pack(white=0):08x}")

    f2 = Color(200, 0, 0)
    # print(f"f2.pack  {f2.pack():08x}")

    assert f1.pack(white=0) == f2.pack()

    print(f"f1.gamma {fancy.gamma_adjust(f1, GAMMA).pack(white=0):08x}")
    print(f"f2.gamma {f2.pack(gamma=True):08x}")

    # assert fancy.gamma_adjust(f1, GAMMA).pack(white=0) == f2.pack(gamma=True)

    def change(c: Color):
        c.with_brightness(0.5)

    benchmark(change, Colors.RED, label="with_brightness")

    def gamma_mine(c: Color):
        pixels[0] = c.gamma()

    benchmark(gamma_mine, Color(200, 0, 0), label="gamma_mine")

    def gamma_fancy(c: fancy.CRGB):
        pixels[0] = fancy.gamma_adjust(c, GAMMA).pack(white=0)

    benchmark(gamma_fancy, fancy.CRGB(200, 0, 0), label="gamma_fancy")

    def mix_mine(c1: Color, c2: Color):
        c1.mix(c2, 0.5).pack()

    benchmark(mix_mine, Colors.RED, Colors.GREEN, label="mix_mine")

    def mix_fancy(c1: fancy.CRGB, c2: fancy.CRGB):
        fancy.mix(c1, c2, 0.5).pack(white=0)

    benchmark(
        mix_fancy, fancy.CRGB(200, 0, 0), fancy.CRGB(0, 200, 0), label="mix_fancy"
    )

    def blink(c: Color):
        pixels[0] = c.values
        pixels.show()
        pixels[0] = c.with_brightness(0.1).values
        pixels.show()

    benchmark(blink, Colors.RED, label="blink")
