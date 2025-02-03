#!/usr/bin/env python3
from the_sign.animations.cube import Cube
from the_sign.animations.rainbow_cycle import RainbowCycle
from the_sign.animations.rainbow_spin import RainbowSpin
from the_sign.animations.shimmer import Shimmer
from the_sign.animations.sparkle import Sparkle
from the_sign.color import Colors, Color, colorwheel

TARGET_FPS = 30

if __name__ == "__main__":
    from .sim import Simulator
    from the_sign.sign import Sign
    from the_sign.animations.blink import Blink

    animations = [
        # Blink(color=Colors.RED, duration=2, frame_rate=TARGET_FPS),
        # Blink(color=Colors.BLUE, duration=1, frame_rate=TARGET_FPS),
        # Shimmer(
        #     c1=Colors.INTELECY,
        #     c2=Colors.INTELECY.with_brightness(0.8),
        #     duration=5,
        #     frame_rate=TARGET_FPS,
        # ),
        # RainbowCycle(duration=0.1, frame_rate=TARGET_FPS),
        # RainbowSpin(frame_rate=TARGET_FPS),
        # Sparkle(base_color=Colors.INTELECY, frame_rate=TARGET_FPS),
        Cube(frame_rate=TARGET_FPS),
    ]

    sim = Simulator(animations, fps=TARGET_FPS)

    # pixels = sim.as_neopixels()
    #
    # pixels[0] = (255, 0, 0)
    # pixels[36] = (0, 255, 0)

    # sign = Sign(sim.as_neopixels(), apply_gamma=False)
    # #
    # sign.ring(3, Colors.RED)
    # sign.ring(2, Colors.ORANGE)
    # sign.ring(1, Colors.YELLOW)
    # sign.ring(0, Colors.PINK)
    #
    # print(Colors.YELLOW)
    # print(f"{colorwheel(28.3):02X}")
    # print(f"{colorwheel(42.5):02X}")
    #
    # for i in range(255):
    #     print(f"{i}: {colorwheel(i):06X}")

    sim.run()
