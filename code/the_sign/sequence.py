from array import array
from the_sign.color import Color, colorwheel
from math import ceil

try:
    from typing import List, Optional
except ImportError:
    pass


def new_buffer(d: float, fps: int) -> array:
    return array("L", [0] * ceil(fps * d))


def gen_fade(
    c1: Color,
    c2: Color,
    d: float,
    fps: int,
    bounce: bool = False,
    apply_gamma: bool = True,
) -> array:
    buffer = new_buffer(d, fps)
    t = len(buffer)
    midpoint = t // 2  # Handle middle frame explicitly when bouncing

    for i in range(t):
        if bounce:
            # Handle symmetric fading logic for "bounce=True"
            if t % 2 == 1 and i == midpoint:  # Odd number of frames and midpoint
                w = 1.0  # Ensure the middle frame reaches c2
            else:
                p = float(i) / t
                w = _bounce(p)
        else:
            # Smooth ramp for "bounce=False"
            p = float(i) / (t - 1)  # This ensures the last frame reaches c2 smoothly.
            w = p

        buffer[i] = c1.mix(c2, w).pack(apply_gamma)

    return buffer


def gen_rainbow(d: float, fps: int) -> array:
    buffer = new_buffer(d, fps)
    t = len(buffer)
    for i in range(t):
        buffer[i] = colorwheel(255 * (float(i) / float(t)))

    return buffer


def _bounce(completed: float, inverse: bool = False) -> float:
    r = 2 * (0.5 - abs(0.5 - completed))  # Symmetric bounce effect
    return 1 - r if inverse else r


def print_seq(seq: array):
    for i in seq:
        print(f"{i:06x} ", end="")
    print()
