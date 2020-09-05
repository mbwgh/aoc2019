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

--- Part Two ---

Once you give them the coordinates, the Elves quickly deploy an Instant
Monitoring Station to the location and discover the worst: there are simply too
many asteroids.

The only solution is complete vaporization by giant laser.

Fortunately, in addition to an asteroid scanner, the new monitoring station
also comes equipped with a giant rotating laser perfect for vaporizing
asteroids. The laser starts by pointing up and always rotates clockwise,
vaporizing any asteroid it hits.

If multiple asteroids are exactly in line with the station, the laser only has
enough power to vaporize one of them before continuing its rotation. In other
words, the same asteroids that can be detected can be vaporized, but if
vaporizing one asteroid makes another one detectable, the newly-detected
asteroid won't be vaporized until the laser has returned to the same position
by rotating a full 360 degrees.

For example, consider the following map, where the asteroid with the new
monitoring station (and laser) is marked X:

.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##

The first nine asteroids to get vaporized, in order, would be:

.#....###24...#..
##...##.13#67..9#
##...#...5.8####.
..#.....X...###..
..#.#.....#....##

Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7)
won't have a chance to be vaporized until the next full rotation. The laser
continues rotating; the next nine to be vaporized are:

.#....###.....#..
##...##...#.....#
##...#......1234.
..#.....X...5##..
..#.9.....8....76

The next nine to be vaporized are then:

.8....###.....#..
56...9#...#.....#
34...7...........
..2.....X....##..
..1..............

Finally, the laser completes its first full rotation (1 through 3), a second
rotation (4 through 8), and vaporizes the last asteroid (9) partway through its
third rotation:

......234.....6..
......1...5.....7
.................
........X....89..
.................

In the large example above (the one with the best monitoring station location
at 11,13):

    The 1st asteroid to be vaporized is at 11,12.
    The 2nd asteroid to be vaporized is at 12,1.
    The 3rd asteroid to be vaporized is at 12,2.
    The 10th asteroid to be vaporized is at 12,8.
    The 20th asteroid to be vaporized is at 16,0.
    The 50th asteroid to be vaporized is at 16,9.
    The 100th asteroid to be vaporized is at 10,16.
    The 199th asteroid to be vaporized is at 9,6.
    The 200th asteroid to be vaporized is at 8,2.
    The 201st asteroid to be vaporized is at 10,9.
    The 299th and final asteroid to be vaporized is at 11,1.

The Elves are placing bets on which will be the 200th asteroid to be vaporized.
Win the bet by determining which asteroid that will be; what do you get if you
multiply its X coordinate by 100 and then add its Y coordinate? (For example,
8,2 becomes 802.)

"""

from math import atan2, gcd, pi, sqrt
from typing import List, Tuple

import numpy as np


def parse_data(data: List[str]) -> np.ndarray:
    """Given the map data, turn it into a matrix of booleans."""
    n_rows = len(data)
    n_cols = len(data[0])
    array = np.empty((n_rows, n_cols), dtype=np.bool_)
    for x in range(n_rows):
        for y in range(n_cols):
            array[x, y] = data[x][y] == "#"

    return array


def square(x_coord, y_coord, radius, rows, cols):
    """Yield a square of coordinates, clamped to [(0, 0), (x_max, y_max)]."""
    def emit(x_val, y_val):
        """Yield the coordinate pair if they are within bounds."""
        if 0 <= x_val < rows and 0 <= y_val < cols:
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


def trajectory(x1, y1, x2, y2, rows, cols):
    """Yield all coordinates that lie on the plane"""
    offset_x, offset_y = offset(x1, y1, x2, y2)
    x, y = x1, y1
    while 0 <= x < rows and 0 <= y < cols:
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
    max_radius = max(matrix.shape) - 1

    encountered_coordinates = set()
    number_of_visible_asteroids = 0
    for radius in range(1, max_radius + 1):
        for x, y in square(x_coord, y_coord, radius, rows, cols):
            if matrix[x, y]:
                if (x, y) in encountered_coordinates:
                    continue
                for traj_x, traj_y in trajectory(x_coord, y_coord, x, y, rows,
                                                 cols):
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


def angle(origin_x, origin_y, x_coord, y_coord):
    """
    Return the angle in radians between the vector that points upwards from
    the given origin, and the vector between the origin and the vector with the
    given coordinates.
    See also: https://stackoverflow.com/questions/14066933/direct-way-of-computing-clockwise-angle-between-2-vectors/16544330#16544330
    """

    v_x, v_y = 0, 1
    w_x, w_y = x_coord - origin_x, y_coord - origin_y

    dot = v_x * w_x + v_y * w_y
    det = v_x * w_y - v_y * w_x

    return atan2(dot, det)


def dist(x1, x2, y1, y2):
    return sqrt((x1 - y1)**2 + (x2 - y2)**2)


def all_angles(origin_x: int, origin_y: int, matrix: np.ndarray) -> List[
        Tuple[int, int, float]]:
    rows, cols = matrix.shape
    angles = []
    for i in range(rows):
        for j in range(cols):
            if matrix[i, j] and (i, j) != (origin_x, origin_y):
                rad = angle(origin_x, origin_y, i, j)
                if rad < 0:
                    rad += 2 * pi
                angles.append((i, j, rad))

    angles.sort(
        key=lambda tup: (tup[2], dist(origin_x, origin_y, tup[0], tup[1])))
    return angles


def max_index(matrix):
    visibilities = calc_visibilities(matrix)
    return np.unravel_index(np.argmax(visibilities), visibilities.shape)


if __name__ == '__main__':
    main1()
