"""
--- Day 13: Care Package ---

As you ponder the solitude of space and the ever-increasing three-hour
roundtrip for messages between you and Earth, you notice that the Space Mail
Indicator Light is blinking. To help keep you sane, the Elves have sent you a
care package.

It's a new game for the ship's arcade cabinet! Unfortunately, the arcade is all
the way on the other end of the ship. Surely, it won't be hard to build your
own - the care package even comes with schematics.

The arcade cabinet runs Intcode software like the game the Elves sent (your
puzzle input). It has a primitive screen capable of drawing square tiles on a
grid. The software draws tiles to the screen with output instructions: every
three output instructions specify the x position (distance from the left), y
position (distance from the top), and tile id. The tile id is interpreted as
follows:

    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a
horizontal paddle tile (1 tile from the left and 2 tiles from the top) and a
ball tile (6 tiles from the left and 5 tiles from the top).

Start the game. How many block tiles are on the screen when the game exits?

--- Part Two ---

The game didn't run because you didn't put in any quarters. Unfortunately, you
did not bring any quarters. Memory address 0 represents the number of quarters
that have been inserted; set it to 2 to play for free.

The arcade cabinet has a joystick that can move left and right. The software
reads the position of the joystick with input instructions:

    If the joystick is in the neutral position, provide 0.
    If the joystick is tilted to the left, provide -1.
    If the joystick is tilted to the right, provide 1.

The arcade cabinet also has a segment display capable of showing a single
number that represents the player's current score. When three output
instructions specify X=-1, Y=0, the third output instruction is not a tile; the
value instead specifies the new score to show in the segment display. For
example, a sequence of output values like -1,0,12345 would show 12345 as the
player's current score.

Beat the game by breaking all the blocks. What is your score after the last
block is broken?

"""

from intcode import Computer
from runner import run


def draw_tile(tile_id):
    """Return a string for the given tile ID."""
    if tile_id == 0:
        return " "
    if tile_id == 1:
        return "#"
    if tile_id == 2:
        return "+"
    if tile_id == 3:
        return "-"
    return "o"


def render_tiles(output):
    """Return the game board as a list of strings."""
    chunks = [output[i:i + 3] for i in range(0, len(output), 3)]
    max_i = max_j = 0
    for i, j, _ in chunks:
        max_i, max_j = max(i, max_i), max(j, max_j)

    matrix = [[None] * (max_j + 1) for _ in range(max_i + 1)]

    for i, j, tile_id in chunks:
        matrix[i][j] = draw_tile(tile_id)

    for i, row in enumerate(matrix):
        matrix[i] = " ".join(row)
    return matrix


def main1():
    """Print the game board and count the block tiles."""
    output = []

    def out(value):
        """Append to output, don't yield."""
        output.append(value)
        return False
    computer = Computer("day13-input", out=out)
    computer.evaluate()
    board = render_tiles(output)
    for line in board:
        print(line)

    num_blocks = 0
    for line in board:
        for tile in line:
            if tile == "+":
                num_blocks += 1
    print(f"{num_blocks} blocks.")


def main2():
    """Beat the game automatically and print the final score."""

    output = []
    joystick = 0
    paddle_x_pos = None
    ball_x_pos = None
    score = 0

    def inp():
        """Return the current joystick position."""
        return joystick

    def out(value):
        """Wait until a triple has been read, then adjust position/joystick."""
        nonlocal paddle_x_pos
        nonlocal ball_x_pos
        nonlocal joystick
        nonlocal output
        nonlocal score
        output.append(value)
        if len(output) == 3:
            i, j, tile_id = output
            output = []
            if i == -1 and j == 0:
                score = tile_id
            elif tile_id == 3:
                paddle_x_pos = i
            elif tile_id == 4:
                ball_x_pos = i

        if paddle_x_pos and ball_x_pos:
            if paddle_x_pos < ball_x_pos:
                joystick = 1
            elif paddle_x_pos > ball_x_pos:
                joystick = -1
            else:
                joystick = 0

        return False

    computer = Computer("day13-input", inp, out)
    computer.memory[0] = 2
    computer.evaluate()

    print(score)


if __name__ == '__main__':
    run(main1, main2)
