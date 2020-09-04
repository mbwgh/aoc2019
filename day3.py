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

--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to
minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each
intersection; choose the intersection where the sum of both wires' steps is
lowest. If a wire visits a position on the grid multiple times, use the steps
value from the first time it visits that position when calculating the total
value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire
has entered to get to that location, including the intersection being
considered. Again consider the example from above:

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

In the above example, the intersection closest to the central port is reached
after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second
wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2
= 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72 U62,R66,U55,R34,D71,R55,D58,R83 = 610
    steps R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?

"""

from re import fullmatch
from runner import run


def dist(left, right):
    """Return the distance of two points."""
    return sum(abs(x - y) for x, y in zip(left, right))


def move(instruction: str, x_coord, y_coord):
    """Transform the given coordinates according to direction and distance."""
    # noinspection RegExpAnonymousGroup
    direction, steps_str = fullmatch(r"([RLUD])(\d+)", instruction).groups()
    steps = int(steps_str)
    if direction == "R":
        return x_coord + steps, y_coord
    if direction == "L":
        return x_coord - steps, y_coord
    if direction == "U":
        return x_coord, y_coord + steps
    return x_coord, y_coord - steps


def read_input():
    """Return a pair of paths, each a sequence of pattern [RLUD]d+."""
    return (line.split(",") for line in open("day3-input").read().splitlines())


def trace(path):
    """
    Return a list of wire positions, starting at 0, 0 and following the
    movements as described by path.
    """
    x_coord = y_coord = 0
    result = []
    for instruction in path:
        x_new, y_new = move(instruction, x_coord, y_coord)
        while (x_coord, y_coord) != (x_new, y_new):
            if x_coord < x_new:
                result.append((x_coord, y_coord))
                x_coord += 1
            elif x_coord > x_new:
                result.append((x_coord, y_coord))
                x_coord -= 1
            elif y_coord < y_new:
                result.append((x_coord, y_coord))
                y_coord += 1
            elif y_coord > y_new:
                result.append((x_coord, y_coord))
                y_coord -= 1
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


def main1():
    """Read `day3-input` and evaluate it."""
    path1, path2 = read_input()
    print(evaluate(path1, path2))


def delay(point, wire1, wire2):
    """
    Return the number of steps from the origin until point, summed for both.
    """
    return wire1.index(point) + wire2.index(point)


def evaluate2(path1, path2):
    """Return the 'closest' crossing according to `delay`."""
    wire1, wire2 = trace(path1), trace(path2)
    crossings = intersection(wire1, wire2)
    return min(delay(point, wire1, wire2) for point in crossings)


def main2():
    """Read `day3-input` and evaluate it."""
    path1, path2 = read_input()
    print(evaluate2(path1, path2))


if __name__ == '__main__':
    run(main1, main2)
