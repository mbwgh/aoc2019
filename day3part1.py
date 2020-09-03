""" --- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus
refuelling station. During the rush back on Earth, the fuel management system
wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are
connected to a central port and extend outward on a grid. You trace the path
each wire takes as it leaves the central port, one wire per line of text (your
puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix
the circuit, you need to find the intersection point closest to the central
port. Because the wires are on a grid, use the Manhattan distance for this
measurement. While the wires do technically cross right at the central port
where they both start, this point does not count, nor does a wire count as
crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the
central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4,
and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

These wires cross at two locations (marked X), but the lower-left one is closer
to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72 U62,R66,U55,R34,D71,R55,D58,R83 =
    distance 159 R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest
intersection?

"""

from re import fullmatch


def dist(xs, ys):
    """Return the distance of two points."""
    return sum(abs(x - y) for x, y in zip(xs, ys))


def move(instruction: str, x, y):
    """Transform the given coordinates according to direction and distance."""
    # noinspection RegExpAnonymousGroup
    direction, steps_str = fullmatch(r"([RLUD])(\d+)", instruction).groups()
    steps = int(steps_str)
    if direction == "R":
        return x + steps, y
    elif direction == "L":
        return x - steps, y
    elif direction == "U":
        return x, y + steps
    else:
        return x, y - steps


def read_input():
    """Return a pair of paths, each a sequence of pattern [RLUD]d+."""
    return (line.split(",") for line in open("day3-input").read().splitlines())


def trace(path):
    """
    Return a list of wire positions, starting at 0, 0 and following the
    movements as described by path.
    """
    x = y = 0
    result = []
    for instruction in path:
        xnew, ynew = move(instruction, x, y)
        while (x, y) != (xnew, ynew):
            if x < xnew:
                result.append((x, y))
                x += 1
            elif x > xnew:
                result.append((x, y))
                x -= 1
            elif y < ynew:
                result.append((x, y))
                y += 1
            elif y > ynew:
                result.append((x, y))
                y -= 1
    return result


def intersection(wire1, wire2):
    """Return the set of common wire positions, but without 0, 0."""
    result = set(wire1).intersection(set(wire2))
    result.remove((0, 0))
    return result


def evaluate(path1, path2):
    """Return the distance of the crossing closest to the origin."""
    wire1, wire2 = trace(path1), trace(path2)
    crossings = intersection(wire1, wire2)
    dists = (dist((x, y), (0, 0)) for x, y in crossings)
    return min(dists)


def main():
    """Read `day3-input` and evaluate it."""
    path1, path2 = read_input()
    print(evaluate(path1, path2))


if __name__ == '__main__':
    main()
