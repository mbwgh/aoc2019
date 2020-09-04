"""
--- Day 10: Monitoring Station ---

You fly into the asteroid belt and reach the Ceres monitoring station. The
Elves here have an emergency: they're having trouble tracking all of the
asteroids and can't be sure they're safe.

The Elves would like to build a new monitoring station in a nearby area of
space; they hand you a map of all of the asteroids in that region (your puzzle
input).

The map indicates whether each position is empty (.) or contains an asteroid
(#). The asteroids are much smaller than they appear on the map, and every
asteroid is exactly in the center of its marked position. The asteroids can be
described with X,Y coordinates where X is the distance from the left edge and Y
is the distance from the top edge (so the top-left corner is 0,0 and the
position immediately to its right is 1,0).

Your job is to figure out which asteroid would be the best place to build a new
monitoring station. A monitoring station can detect any asteroid to which it
has direct line of sight - that is, there cannot be another asteroid exactly
between them. This line of sight can be at any angle, not just lines aligned to
the grid or diagonally. The best location is the asteroid that can detect the
largest number of other asteroids.

For example, consider the following map:

.#..#
.....
#####
....#
...##

The best location for a new monitoring station on this map is the highlighted
asteroid at 3,4 because it can detect 8 asteroids, more than any other
location. (The only asteroid it cannot detect is the one at 1,0; its view of
this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse
locations; they can detect 7 or fewer other asteroids. Here is the number of
other asteroids a monitoring station on each asteroid could detect:

.7..7
.....
67775
....7
...87

Here is an asteroid (#) and some examples of the ways its line of sight might
be blocked. If there were another asteroid at the location of a capital letter,
the locations marked with the corresponding lowercase letter would be blocked
and could not be detected:

#.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c

Here are some larger examples:

    Best is 5,8 with 33 other asteroids detected:

    ......#.#.
    #..#.#....
    ..#######.
    .#.#.###..
    .#..#.....
    ..#....#.#
    #..#....#.
    .##.#..###
    ##...#..#.
    .#....####

    Best is 1,2 with 35 other asteroids detected:

    #.#...#.#.
    .###....#.
    .#....#...
    ##.#.#.#.#
    ....#.#.#.
    .##..###.#
    ..#...##..
    ..##....##
    ......#...
    .####.###.

    Best is 6,3 with 41 other asteroids detected:

    .#..#..###
    ####.###.#
    ....###.#.
    ..###.##.#
    ##.##.#.#.
    ....###..#
    ..#.#..#.#
    #..#.#.###
    .##...##.#
    .....#.#..

    Best is 11,13 with 210 other asteroids detected:

    .#..##.###...#######
    ##.############..##.
    .#.######.########.#
    .###.#######.####.#.
    #####.##.#.##.###.##
    ..#####..#.#########
    ####################
    #.####....###.#.#.##
    ##.#################
    #####.##.###..####..
    ..######..##.#######
    ####.##.####...##..#
    .#####..#.######.###
    ##...#.##########...
    #.##########.#######
    .####.#.###.###.#.##
    ....##.##.###..#####
    .#.#.###########.###
    #.#.#.#####.####.###
    ###.##.####.##.#..##

Find the best location for a new monitoring station. How many other asteroids
can be detected from that location?

"""

from math import gcd
from typing import List

import numpy as np


def parse_data(data: List[str]) -> np.ndarray:
    """Given the map data, turn it into a matrix of booleans."""
    n_rows = len(data)
    n_cols = len(data[0])
    array = np.empty((n_rows, n_cols), dtype=np.bool_)
    for x in range(n_cols):
        for y in range(n_rows):
            array[x, y] = data[y][x] == "#"

    return array


def square(x_coord, y_coord, radius, x_max, y_max):
    """Yield a square of coordinates, clamped to [(0, 0), (x_max, y_max)]."""
    def emit(x_val, y_val):
        """Yield the coordinate pair if they are within bounds."""
        if 0 <= x_val <= x_max and 0 <= y_val <= y_max:
            yield x_val, y_val

    y_value = y_coord - radius
    for x_value in range(x_coord - radius, x_coord + radius):
        yield from emit(x_value, y_value)

    x_value = x_coord + radius
    for y_value in range(y_coord - radius, y_coord + radius):
        yield from emit(x_value, y_value)

    y_value = y_coord + radius
    for x_value in range(x_coord + radius, x_coord - radius, -1):
        yield from emit(x_value, y_value)

    x_value = x_coord - radius
    for y_value in range(y_coord + radius, y_coord - radius, -1):
        yield from emit(x_value, y_value)


def offset(x1, y1, x2, y2):
    """Calculate the smallest integral multiple of the offset vector."""
    offset_x, offset_y = x2 - x1, y2 - y1
    divisor = gcd(offset_x, offset_y)
    return offset_x // divisor, offset_y // divisor


def trajectory(x1, y1, x2, y2, x_max, y_max):
    """Yield all coordinates that lie on the plane"""
    offset_x, offset_y = offset(x1, y1, x2, y2)
    x, y = x1, y1
    while 0 <= x <= x_max and 0 <= y <= y_max:
        yield x, y
        x, y = x + offset_x, y + offset_y


def visibility(x_coord, y_coord, matrix: np.ndarray):
    """
    Calculate the number of visible asteroids at this point.
    If there is no asteroid at this location, return 0.
    """
    if not matrix[x_coord, y_coord]:
        return 0

    rows, cols = matrix.shape
    x_max = cols - 1
    y_max = rows - 1
    max_radius = max(matrix.shape) - 1

    encountered_coordinates = set()
    number_of_visible_asteroids = 0
    for radius in range(1, max_radius + 1):
        for x, y in square(x_coord, y_coord, radius, x_max, y_max):
            if matrix[x, y]:
                if (x, y) in encountered_coordinates:
                    continue
                for traj_x, traj_y in trajectory(x_coord, y_coord, x, y, x_max,
                                                 y_max):
                    encountered_coordinates.add((traj_x, traj_y))
                number_of_visible_asteroids += 1
    return number_of_visible_asteroids


def calc_visibilities(matrix):
    """Calculate the number of visible asteroids at each point."""
    rows, cols = matrix.shape
    result = np.empty(matrix.shape, dtype=np.int_)
    for i in range(rows):
        for j in range(cols):
            result[i, j] = visibility(i, j, matrix)
    return result


def main1():
    """Print the maximum number of visible asteroids."""
    data = open("day10-input").read().splitlines()
    matrix = parse_data(data)
    visibilities = calc_visibilities(matrix)
    print(np.max(visibilities))


if __name__ == '__main__':
    main1()
