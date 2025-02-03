import math
import random
from typing import Union, Tuple, List

import pygame
import sys
from the_sign import Sign
from the_sign import NeoPixelInterface
from the_sign.animations import Animation
from the_sign.color import Color

BLACK = (0, 0, 0)
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
DARK_GREY = (70, 70, 70)  # for wiring


class Simulator:
    def __init__(self, animations: List[Animation], fps: int = 25):
        self._animations = animations

        if len(self._animations) == 0:
            self._animations = [Animation(frame_rate=1)]

        self._current_animation = 0
        self.fps = fps
        self.n = 37
        self.cells = []

        self._r_grid = 3  # grid radius (axial coordinates)
        self._r_draw = 1.0  # provisional drawn cell size

        for q in range(-self._r_grid, self._r_grid + 1):
            r_min = max(-self._r_grid, -q - self._r_grid)
            r_max = min(self._r_grid, -q + self._r_grid)
            for r in range(r_min, r_max + 1):
                cx = self._r_draw * 1.5 * q
                cy = self._r_draw * math.sqrt(3) * (r + q / 2)
                center = (cx, cy)
                poly = flat_top_hexagon(center, self._r_draw)
                self.cells.append(
                    {
                        "q": q,
                        "r": r,
                        "center": center,
                        "poly": poly,
                        # 'dot' index will be added next.
                    }
                )

        # Assign wiring (dot) indices in zig–zag order.
        cols = {}
        for cell in self.cells:
            cols.setdefault(cell["q"], []).append(cell)

        for q in cols:
            cols[q].sort(key=lambda c: c["r"])

        ordered_qs = sorted(cols.keys(), reverse=True)
        dot_index = 0

        for col_index, q in enumerate(ordered_qs):
            col_cells = cols[q]

            if col_index % 2 == 0:
                ordered_cells = sorted(col_cells, key=lambda c: c["r"], reverse=True)
            else:
                ordered_cells = sorted(col_cells, key=lambda c: c["r"])

            for cell in ordered_cells:
                cell["dot"] = dot_index
                dot_index += 1

        # Compute overall bounding box (in world coordinates).
        self._min_x = min(v[0] for cell in self.cells for v in cell["poly"])
        self._max_x = max(v[0] for cell in self.cells for v in cell["poly"])
        self._min_y = min(v[1] for cell in self.cells for v in cell["poly"])
        self._max_y = max(v[1] for cell in self.cells for v in cell["poly"])
        self._bbox_width = self._max_x - self._min_x
        self._bbox_height = self._max_y - self._min_y

        self.sign = Sign(self.as_neopixels(), apply_gamma=False)

    def as_neopixels(self) -> NeoPixelInterface:
        return self

    def __getitem__(self, index: int) -> Tuple[int, int, int]:
        for cell in self.cells:
            if cell["dot"] == index:
                return cell["color"]
        else:
            raise IndexError(f"No cell with dot index {index}")

    def __setitem__(self, index: int, color: Union[Tuple[int, int, int], int]) -> None:
        if isinstance(color, int):
            wv = color >> 24
            if wv > 0:
                color = wv, wv, wv
            else:
                color = (
                    (color & 0xFF0000) >> 16,
                    (color & 0x00FF00) >> 8,
                    color & 0x0000FF,
                )
        elif isinstance(color, Color):
            if color.w > 0:
                color = color.w, color.w, color.w
            else:
                color = color.r, color.g, color.b
        else:
            # we have RGBW
            if len(color) == 4:
                # cheat and just use the W
                # note: this won't handle something like (255, 0, 0, 255)
                if color[3] > 0:
                    color = color[3], color[3], color[3]
                else:
                    color = color[:3]

        for cell in self.cells:
            if cell["dot"] == index:
                cell["color"] = color
                return
        else:
            raise IndexError(f"No cell with dot index {index}")

    def fill(self, color: Union[Tuple[int, int, int], int]) -> None:
        for i in range(len(self.cells)):
            self[i] = color

    def show(self):
        return

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1024, 1024), pygame.RESIZABLE)
        pygame.display.set_caption("TheSign Simulator")
        clock = pygame.time.Clock()
        font_size = 40
        font = pygame.font.SysFont(None, font_size)

        # For frame number calculation.
        start_time = pygame.time.get_ticks()

        # ===== Main Loop =====

        running = True

        animation = self._animations[self._current_animation]
        animation.setup(self.sign)

        while running:
            animation = self._animations[self._current_animation]

            current_time = pygame.time.get_ticks()
            elapsed = (current_time - start_time) / 1000.0  # seconds elapsed
            frame_number = int(self.fps * elapsed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Press 'q' to quit.
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self._current_animation = (self._current_animation - 1) % len(
                            self._animations
                        )
                        animation = self._animations[self._current_animation]
                        animation.setup(self.sign)
                    elif event.key == pygame.K_RIGHT:
                        self._current_animation = (self._current_animation + 1) % len(
                            self._animations
                        )
                        animation = self._animations[self._current_animation]
                        animation.setup(self.sign)

            # Execute the animation (updates cell colors).
            animation.exec(self.sign, frame_number)

            # Compute scaling and offsets so the sign occupies ~90% of the window.
            win_width, win_height = screen.get_size()
            scale = 0.9 * min(
                win_width / self._bbox_width, win_height / self._bbox_height
            )
            grid_center_x = (self._min_x + self._max_x) / 2
            grid_center_y = (self._min_y + self._max_y) / 2
            offset_x = win_width / 2 - scale * grid_center_x
            offset_y = win_height / 2 - scale * grid_center_y

            screen.fill(BLACK)

            # --- Draw Wiring as Base Layer ---
            sorted_cells = sorted(self.cells, key=lambda c: c["dot"])
            base_wire_points = [
                transform(c["center"], scale, (offset_x, offset_y))
                for c in sorted_cells
            ]
            pygame.draw.lines(screen, DARK_GREY, False, base_wire_points, width=3)

            # --- Draw Each Cell ---
            for cell in self.cells:
                poly_screen = [
                    transform(v, scale, (offset_x, offset_y)) for v in cell["poly"]
                ]
                pygame.draw.polygon(screen, GREY, poly_screen, width=3)

                center_screen = transform(cell["center"], scale, (offset_x, offset_y))
                gradient_radius = int(scale * 0.5 * self._r_draw)  # 50% of cell width.
                color = cell.get("color", (0, 0, 0))
                if color != (0, 0, 0):
                    draw_gradient_circle(
                        screen, center_screen, gradient_radius, color, steps=20
                    )

                br = poly_screen[3]
                bl = poly_screen[4]
                bottom_mid = ((br[0] + bl[0]) / 2, (br[1] + bl[1]) / 2)
                text_str = str(cell["dot"])
                text_surf = font.render(text_str, True, DARK_GREY)
                text_rect = text_surf.get_rect()
                margin = 5
                text_rect.midbottom = (bottom_mid[0], bottom_mid[1] - margin)
                screen.blit(text_surf, text_rect)

            # --- Redraw Wiring on Top for Off (Black) Pixels ---
            for i in range(len(sorted_cells) - 1):
                cell1 = sorted_cells[i]
                cell2 = sorted_cells[i + 1]
                if cell1.get("color", (0, 0, 0)) == (0, 0, 0) or cell2.get(
                    "color", (0, 0, 0)
                ) == (0, 0, 0):
                    pt1 = transform(cell1["center"], scale, (offset_x, offset_y))
                    pt2 = transform(cell2["center"], scale, (offset_x, offset_y))
                    pygame.draw.line(screen, DARK_GREY, pt1, pt2, width=3)

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()
        sys.exit()


def flat_top_hexagon(center, R):
    """
    Given a center (cx, cy) and a hexagon "size" R (distance from center to vertex),
    return a list of six vertices (as (x, y) tuples) for a flat–top hexagon.
    (This hexagon has horizontal top and bottom edges.)

    Vertices (in order):
      v0: (cx - R/2,       cy - (sqrt3/2)*R)
      v1: (cx + R/2,       cy - (sqrt3/2)*R)
      v2: (cx + R,         cy)
      v3: (cx + R/2,       cy + (sqrt3/2)*R)
      v4: (cx - R/2,       cy + (sqrt3/2)*R)
      v5: (cx - R,         cy)
    """
    sqrt3 = math.sqrt(3)
    cx, cy = center
    return [
        (cx - 0.5 * R, cy - (sqrt3 / 2) * R),
        (cx + 0.5 * R, cy - (sqrt3 / 2) * R),
        (cx + R, cy),
        (cx + 0.5 * R, cy + (sqrt3 / 2) * R),
        (cx - 0.5 * R, cy + (sqrt3 / 2) * R),
        (cx - R, cy),
    ]


def transform(pt, scale, offset):
    """Apply scale and offset to a point (pt is a tuple (x, y))."""
    x, y = pt
    offx, offy = offset
    return (x * scale + offx, y * scale + offy)


def draw_gradient_circle(surface, center, max_radius, color, steps=20):
    """
    Draws a radial gradient circle on 'surface' at position 'center'
    with an outer radius of 'max_radius'. The 'color' is an (R, G, B) tuple.

    This function draws 'steps' concentric circles. For each ring i (i = steps (outer)
    down to i = 1 (inner)) the opacity is linearly interpolated:
         alpha = int(255 * ((steps - i + 1) / steps))
    """
    r, g, b = color
    for i in range(steps, 0, -1):
        radius = int(max_radius * i / steps)
        alpha = int(255 * ((steps - i + 1) / steps))
        temp = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp, (r, g, b, alpha), (max_radius, max_radius), radius)
        surface.blit(temp, (center[0] - max_radius, center[1] - max_radius))
