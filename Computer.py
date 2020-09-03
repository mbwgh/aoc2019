"""The IntCode computer."""

import os
from typing import Callable, Union, Sequence


class Computer:
    """
    An IntCode Computer supporting opcodes 1-8, 99.
    """
    def __init__(self, tape: Union[Sequence[int], str], inp: Callable[[], int],
                 out: Callable[[int], bool]):
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
            self.memory = [int(n) for n in tape.split(",")]
        else:
            self.memory = list(tape)
        self.ip = 0
        self.inp = inp
        self.out = out
        self.opcode = None
        self.modes = None

    def fetch(self):
        """Update opcode and operation modes."""
        number = self.memory[self.ip]
        self.opcode = number % 100
        self.modes = tuple(number // 10**i % 10 for i in (2, 3, 4))

    def read(self, offset):
        """
        Read a value either directly or indirectly, depending on the current
        opcode's modes. The offset is taken as the parameter number of the
        current instruction as well. For instance, ``offset=1`` refers to the
        1st parameter, and its mode is taken into consideration.
        :param offset: The offset from the instruction pointer.
        :return: The value either at ``self.ip + offset`` or at the address.
        """
        mode = self.modes[offset - 1]
        addr = self.memory[self.ip + offset] if mode == 0 else self.ip + offset
        return self.memory[addr]

    def write(self, offset, value):
        """Dually to ``self.read``, write a value directly or indirectly."""
        mode = self.modes[offset - 1]
        addr = self.memory[self.ip + offset] if mode == 0 else self.ip + offset
        self.memory[addr] = value

    def evaluate(self) -> None:
        """
        Start processing the program until either the HALT code (99) is
        reached, or the program yields after having written to ``self.out``.
        """
        self.fetch()
        while self.opcode != 99:
            if self.opcode == 1:
                x = self.read(1)
                y = self.read(2)
                self.write(3, x + y)
                self.ip += 4
            elif self.opcode == 2:
                x = self.read(1)
                y = self.read(2)
                self.write(3, x * y)
                self.ip += 4
            elif self.opcode == 3:
                x = self.inp()
                self.write(1, x)
                self.ip += 2
            elif self.opcode == 4:
                x = self.read(1)
                should_yield = self.out(x)
                self.ip += 2
                if should_yield:
                    return
            elif self.opcode == 5:
                x = self.read(1)
                self.ip = self.read(2) if x != 0 else self.ip + 3
            elif self.opcode == 6:
                x = self.read(1)
                self.ip = self.read(2) if x == 0 else self.ip + 3
            elif self.opcode == 7:
                x = self.read(1)
                y = self.read(2)
                self.write(3, 1 if x < y else 0)
                self.ip += 4
            elif self.opcode == 8:
                x = self.read(1)
                y = self.read(2)
                self.write(3, 1 if x == y else 0)
                self.ip += 4
            else:
                raise ValueError(f"unexpected input: {self.memory[self.ip]}")
            self.fetch()

    def has_halted(self):
        """Return whether the HALT code has already been encountered."""
        return self.opcode == 99
