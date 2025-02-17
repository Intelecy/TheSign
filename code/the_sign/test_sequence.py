from .color import Colors
from .sequence import gen_fade, print_seq, gen_rainbow


def test_fade():
    buffer = gen_fade(Colors.BLACK, Colors.RED, 1.0, 10, apply_gamma=False)

    assert len(buffer) == 10
    assert buffer[0] == Colors.BLACK.pack()
    assert buffer[-1] == Colors.RED.pack()

    buffer = gen_fade(Colors.BLACK, Colors.RED, 1.0, 11, apply_gamma=False)

    assert len(buffer) == 11
    assert buffer[0] == Colors.BLACK.pack()
    assert buffer[-1] == Colors.RED.pack()

    buffer = gen_fade(Colors.BLACK, Colors.RED, 1.0, 10, bounce=True, apply_gamma=False)

    assert len(buffer) == 10
    assert buffer[0] == Colors.BLACK.pack()
    assert buffer[-1] != Colors.BLACK.pack()
    assert buffer[len(buffer) // 2] == Colors.RED.pack()
    assert buffer[1] == buffer[-1]

    buffer = gen_fade(Colors.BLACK, Colors.RED, 1.0, 11, bounce=True, apply_gamma=False)

    assert len(buffer) == 11
    assert buffer[0] == Colors.BLACK.pack()
    assert buffer[-1] != Colors.BLACK.pack()
    assert buffer[len(buffer) // 2] == Colors.RED.pack()
    assert buffer[1] == buffer[-1]

    buffer = gen_fade(Colors.BLACK, Colors.RED, 256, 1, apply_gamma=False)
    assert len(buffer) == 256

    for i in range(len(buffer) - 1):
        assert (
            buffer[i + 1] - buffer[i] == 0x010000
        ), f"i={i} {buffer[i + 1] - buffer[i]}"

    assert buffer[0] == Colors.BLACK.pack()
    assert buffer[-1] == Colors.RED.pack()
    assert buffer[len(buffer) // 2] == Colors.RED.mix(Colors.BLACK, 0.5).pack()

    buffer = gen_fade(Colors.BLACK, Colors.WHITE, 256, 1, apply_gamma=False)
    print()
    print_seq(buffer)

    return


# def test_rainbow():
#     buffer = gen_rainbow(256, 1)
#     assert len(buffer) == 256
#     print()
#     print_seq(buffer)
#     return


def test_mix():
    c1 = Colors.BLACK
    c2 = Colors.RED

    assert c1.mix(c2, 0.0).pack() == 0x000000
    assert c1.mix(c2, 1.0).pack() == 0xFF0000
    assert c1.mix(c2, 0.5).pack() == 0x800000
    assert c2.mix(c1, 0.5).pack() == 0x800000

    assert c1.mix(c2, 0.004).pack() == 0x010000
