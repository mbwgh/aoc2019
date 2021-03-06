"""
--- Day 11: Space Police ---

On the way to Jupiter, you're pulled over by the Space Police.

"Attention, unmarked spacecraft! You are in violation of Space Law! All
spacecraft must have a clearly visible registration identifier! You have 24
hours to comply or be sent to Space Jail!"

Not wanting to be sent to Space Jail, you radio back to the Elves on Earth for
help. Although it takes almost three hours for their reply signal to reach you,
they send instructions for how to power up the emergency hull painting robot
and even provide a small Intcode program (your puzzle input) that will cause it
to paint your ship appropriately.

There's just one problem: you don't have an emergency hull painting robot.

You'll need to build a new emergency hull painting robot. The robot needs to be
able to move around on the grid of square panels on the side of your ship,
detect the color of its current panel, and paint its current panel black or
white. (All of the panels are currently black.)

The Intcode program will serve as the brain of the robot. The program uses
input instructions to access the robot's camera: provide 0 if the robot is over
a black panel or 1 if the robot is over a white panel. Then, the program will
output two values:

    First, it will output a value indicating the color to paint the panel the
    robot is over: 0 means to paint the panel black, and 1 means to paint the
    panel white.
    Second, it will output a value indicating the direction the robot should
    turn: 0 means it should turn left 90 degrees, and 1 means it should turn
    right 90 degrees.

After the robot turns, it should always move forward exactly one panel. The
robot starts facing up.

The robot will continue running for a while like this and halt when it is
finished drawing. Do not restart the Intcode computer inside the robot during
this process.

For example, suppose the robot is about to start running. Drawing black panels
as ., white panels as #, and the robot pointing the direction it is facing (< ^
> v), the initial state and region near the robot looks like this:

.....
.....
..^..
.....
.....

The panel under the robot (not visible here because a ^ is shown instead) is
also black, and so any input instructions at this point should be provided 0.
Suppose the robot eventually outputs 1 (paint white) and then 0 (turn left).
After taking these actions and moving forward one panel, the region now looks
like this:

.....
.....
.<#..
.....
.....

Input instructions should still be provided 0. Next, the robot might output 0
(paint black) and then 0 (turn left):

.....
.....
..#..
.v...
.....

After more outputs (1,0, 1,0):

.....
.....
..^..
.##..
.....

The robot is now back where it started, but because it is now on a white panel,
input instructions should be provided 1. After several more outputs (0,1, 1,0,
1,0), the area looks like this:

.....
..<#.
...#.
.##..
.....

Before you deploy the robot, you should probably have an estimate of the area
it will cover: specifically, you need to know the number of panels it paints at
least once, regardless of color. In the example above, the robot painted 6
panels at least once. (It painted its starting panel twice, but that panel is
still only counted once; it also never painted the panel it ended on.)

Build a new emergency hull painting robot and run the Intcode program on it.
How many panels does it paint at least once?

"""

from enum import IntEnum

from intcode import Computer
from runner import run


class Direction(IntEnum):
    """A direction can be used to move or rotate the robot."""
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    def move(self, x, y):
        """Return the coordinates shifted according to this direction."""
        if self == Direction.UP:
            return x, y + 1
        if self == Direction.LEFT:
            return x - 1, y
        if self == Direction.DOWN:
            return x, y - 1
        return x + 1, y

    def turn_left(self):
        """Return a direction that has been rotated to the left."""
        return Direction((self + 1) % 4)

    def turn_right(self):
        """Return a direction that has been rotated to the right."""
        return Direction((((self - 1) % 4) + 4) % 4)


class Robot:
    """The hull painting robot."""
    def __init__(self, program, start_color=0):
        self.position = 0, 0
        self.direction = Direction.UP
        self.encountered_positions = {(0, 0): start_color}
        self.computer_output = []

        def out(value):
            """The function the intcode computer should use for output."""
            self.computer_output.append(value)
            return True

        def get_color():
            """The function the intcode computer should use to read input."""
            return self.encountered_positions.get(self.position, 0)

        self.computer = Computer(program, get_color, out)

    def run(self):
        """
        Keep running the computer until it halts, paint and move according to
        its output.
        """
        while not self.computer.has_halted():
            self.computer.evaluate()
            if self.computer.has_halted():
                break
            self.computer.evaluate()
            [color, direction] = self.computer_output
            self.computer_output.clear()
            self.encountered_positions[self.position] = color
            self.direction = self.direction.turn_right() if direction \
                else self.direction.turn_left()
            self.position = self.direction.move(*self.position)


def render(encountered_positions):
    """Take the robot's result and return a string ready for printing."""
    min_x = min(x for x, y in encountered_positions.keys())
    max_x = max(x for x, y in encountered_positions.keys())
    min_y = min(y for x, y in encountered_positions.keys())
    max_y = max(y for x, y in encountered_positions.keys())

    tiles = []
    for i in range(min_x, max_x + 1):
        row = []
        for j in range(min_y, max_y + 1):
            color = encountered_positions.get((i, j), 0)
            row.append("##" if color else "  ")
        tiles.append("".join(row))

    return "\n".join(tiles)


def main1():
    """Traverse the hull and print the number of encountered positions."""
    robot = Robot("day11-input")
    robot.run()
    print(len(robot.encountered_positions))


def main2():
    """Display the message on the hull."""
    robot = Robot("day11-input", 1)
    robot.run()
    print(render(robot.encountered_positions))


if __name__ == '__main__':
    run(main1, main2)
