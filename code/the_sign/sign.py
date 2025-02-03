try:
    from typing import Protocol, Union, Tuple, List
    from the_sign.color import ColorUnion
except ImportError:

    class Protocol:
        pass

    class ColorUnion:
        pass


from the_sign.color import Color, Colors


class NeoPixelInterface(Protocol):
    n: int  # Number of pixels

    def __getitem__(self, index: int) -> Tuple[int, int, int]: ...
    def __setitem__(
        self, index: int, color: Union[Tuple[int, int, int], int]
    ) -> None: ...
    def fill(self, color: Union[Tuple[int, int, int], int]) -> None: ...
    def show(self) -> None: ...


class Sign:
    _rings = [
        [18],
        [17, 12, 11, 19, 24, 25],
        [16, 13, 5, 6, 7, 10, 20, 23, 31, 30, 29, 26],
        [15, 14, 4, 3, 2, 1, 0, 8, 9, 21, 22, 32, 33, 34, 35, 36, 28, 27],
    ]

    def __init__(
        self,
        pixels: NeoPixelInterface,
        apply_gamma: bool = True,
    ):
        self._pixels = pixels
        self._apply_gamma = apply_gamma
        self._n = pixels.n

    def fill(self, color: Color):
        if self._apply_gamma:
            c = color.with_gamma()
        else:
            c = color

        self._pixels.fill((c.r, c.g, c.b, c.w))

    def clear(self):
        self.fill(Colors.BLACK)
        self.show()

    def show(self):
        self._pixels.show()

    def ring(
        self,
        index: int,
        val: Union[ColorUnion | Color],
    ):
        for i in self._rings[index]:
            self[i] = val

    @property
    def n(self) -> int:
        return self._n

    def __len__(self) -> int:
        return self._n

    def __setitem__(
        self,
        index: int,
        val: Union[ColorUnion | Color],
    ):
        if isinstance(val, Color):
            c = val.with_gamma()
            self._pixels[index] = c.r, c.g, c.b, c.w
        else:
            self._pixels[index] = val

    @property
    def ring0(self) -> List[int]:
        return self._rings[0]

    @ring0.setter
    def ring0(self, val: Union[ColorUnion | Color]):
        for i in self.ring0:
            self[i] = val

    @property
    def ring1(self) -> List[int]:
        return self._rings[1]

    @ring1.setter
    def ring1(self, val: Union[ColorUnion | Color]):
        for i in self.ring1:
            self[i] = val

    @property
    def ring2(self) -> List[int]:
        return self._rings[2]

    @ring2.setter
    def ring2(self, val: Union[ColorUnion | Color]):
        for i in self.ring2:
            self[i] = val

    @property
    def ring3(self) -> List[int]:
        return self._rings[3]

    @ring3.setter
    def ring3(self, val: Union[ColorUnion | Color]):
        for i in self.ring3:
            self[i] = val
