"""
--- Part Two ---

Now you're ready to decode the image. The image is rendered by stacking the
layers and aligning the pixels with the same positions in each layer. The
digits indicate the color of the corresponding pixel: 0 is black, 1 is white,
and 2 is transparent.

The layers are rendered with the first layer in front and the last layer in
back. So, if a given position has a transparent pixel in the first and second
layers, a black pixel in the third layer, and a white pixel in the fourth
layer, the final image would have a black pixel at that position.

For example, given an image 2 pixels wide and 2 pixels tall, the image data
0222112222120000 corresponds to the following image layers:

Layer 1: 02
         22

Layer 2: 11
         22

Layer 3: 22
         12

Layer 4: 00
         00

Then, the full image can be found by determining the top visible pixel in each
position:

    The top-left pixel is black because the top layer is 0.
    The top-right pixel is white because the top layer is 2 (transparent), but
    the second layer is 1.
    The bottom-left pixel is white because the top two layers are 2, but the
    third layer is 1.
    The bottom-right pixel is black because the only visible pixel in that
    position is 0 (from layer 4).

So, the final image looks like this:

01
10

What message is produced after decoding your image?

"""

from day8part1 import load_data

import numpy as np


def pixel_at(i, layers):
    """Skip transparent layers and return the first non-transparent pixel."""
    for layer in layers:
        pixel = layer[i]
        if pixel == 2:
            continue
        return pixel


def decode_data(layers):
    """Calculate each pixel and return a properly-shaped picture."""
    n = len(layers[0])
    result = np.empty(n)
    for i in range(n):
        result[i] = pixel_at(i, layers)
    return result.reshape(6, 25)


def draw(picture_data):
    """Render the picture by turning it into a list of strings."""
    data = picture_data.tolist()
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            row[j] = "." if row[j] == 0 else "|"
        data[i] = "".join(row)
    return data


def main():
    """Decode and display the picture."""
    values = tuple(int(c) for c in open("day8-input").read().rstrip("\n"))
    layers = load_data(25, 6, values)
    lines = draw(decode_data(layers))
    for line in lines:
        print(line)


if __name__ == '__main__':
    main()
