#!/usr/bin/env python3
from the_sign import images
from the_sign.animations.shimmer import Shimmer
from the_sign.animations.static import Static

from the_sign.color import Colors, Color, colorwheel

TARGET_FPS = 2 * (1_000 // 37)

if __name__ == "__main__":
    from .sim import Simulator

    animations = [
        Static(img=images.settlers, frame_rate=TARGET_FPS),
        # Blink(color=Colors.RED, duration=2, frame_rate=TARGET_FPS),
        # Blink(color=Colors.BLUE, duration=1, frame_rate=TARGET_FPS),
        Shimmer(
            c1=Colors.INTELECY,
            c2=Colors.INTELECY.with_brightness(0.8),
            duration=12,
            frame_rate=TARGET_FPS,
        ),
        # RainbowCycle(duration=0.1, frame_rate=TARGET_FPS),
        # RainbowSpin(frame_rate=TARGET_FPS),
        # Sparkle(base_color=Colors.INTELECY, frame_rate=TARGET_FPS),
        # Cube(frame_rate=TARGET_FPS),
        # Heart(frame_rate=TARGET_FPS),
        # Smile(frame_rate=TARGET_FPS),
        # KnightRider(duration=2, frame_rate=TARGET_FPS),
        # CalcSequence(color=Colors.INTELECY, duration=5, frame_rate=TARGET_FPS),
    ]

    sim = Simulator(animations, fps=TARGET_FPS)
    sim.run()
