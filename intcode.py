"""The IntCode computer."""

import os
from typing import Callable, Union, Sequence


class Computer:
    """
    An IntCode Computer supporting opcodes 1-8, 99.
    """

    def __init__(self, tape: Union[Sequence[int], str],
                 inp: Callable[[], int] = None,
                 out: Callable[[int], bool] = None):
        """
        Initialize the Computer without running it yet.
        :param tape: Input file, a program string or the parsed program.
        :param inp: Source for input values.
        :param out: Sink for output. May return true if the computation should
                    yield.
        """
        if isinstance(tape, str):
            if os.path.isfile(tape):
                tape = open(tape).read()
            self.memory = {ix: int(n) for ix, n in enumerate(tape.split(","))}
        else:
            self.memory = dict(enumerate(tape))
        self.iptr = 0
        self.inp = inp
        self.out = out
        self.opcode = None
        self.modes = None
        self.base = 0

    def fetch(self):
        """Update opcode and operation modes."""
        number = self.memory[self.iptr]
        self.opcode = number % 100
        self.modes = tuple(number // 10**i % 10 for i in (2, 3, 4))

    def get_address(self, offset):
        """Calculate the address for ``self.read`` and ``self.write``."""
        mode = self.modes[offset - 1]
        if mode == 0:
            return self.memory[self.iptr + offset]
        if mode == 1:
            return self.iptr + offset
        return self.memory[self.iptr + offset] + self.base

    def read(self, offset):
        """
        Read a value according to the current mode for the specified offset.
        The offset is taken as the parameter number of the
        current instruction. For instance, ``offset=1`` refers to the
        1st parameter, and its mode is taken into consideration.
        :param offset: The offset from the instruction pointer.
        :return: The value either at an address.
        """
        addr = self.get_address(offset)
        return self.memory[addr] if addr in self.memory else 0

    def write(self, offset, value):
        """Dually to ``self.read``, write a value according to mode."""
        addr = self.get_address(offset)
        self.memory[addr] = value

    def evaluate(self) -> None:
        """
        Start processing the program until either the HALT code (99) is
        reached, or the program yields after having written to ``self.out``.
        """
        self.fetch()
        while self.opcode != 99:
            if self.opcode == 1:
                arg1 = self.read(1)
                arg2 = self.read(2)
                self.write(3, arg1 + arg2)
                self.iptr += 4
            elif self.opcode == 2:
                arg1 = self.read(1)
                arg2 = self.read(2)
                self.write(3, arg1 * arg2)
                self.iptr += 4
            elif self.opcode == 3:
                arg1 = self.inp()
                self.write(1, arg1)
                self.iptr += 2
            elif self.opcode == 4:
                arg1 = self.read(1)
                should_yield = self.out(arg1)
                self.iptr += 2
                if should_yield:
                    return
            elif self.opcode == 5:
                arg1 = self.read(1)
                self.iptr = self.read(2) if arg1 != 0 else self.iptr + 3
            elif self.opcode == 6:
                arg1 = self.read(1)
                self.iptr = self.read(2) if arg1 == 0 else self.iptr + 3
            elif self.opcode == 7:
                arg1 = self.read(1)
                arg2 = self.read(2)
                self.write(3, 1 if arg1 < arg2 else 0)
                self.iptr += 4
            elif self.opcode == 8:
                arg1 = self.read(1)
                arg2 = self.read(2)
                self.write(3, 1 if arg1 == arg2 else 0)
                self.iptr += 4
            elif self.opcode == 9:
                arg1 = self.read(1)
                self.base += arg1
                self.iptr += 2
            else:
                raise ValueError(f"unexpected input: {self.memory[self.iptr]}")
            self.fetch()

    def has_halted(self):
        """Return whether the HALT code has already been encountered."""
        return self.opcode == 99
