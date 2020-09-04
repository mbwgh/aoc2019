"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a
password. The Elves had written the password on a sticky note, but someone
threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number. The value is within the range given in your
    puzzle input. Two adjacent digits are the same (like 22 in 122345). Going
    from left to right, the digits never decrease; they only ever increase or
    stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases). 223450 does not
    meet these criteria (decreasing pair of digits 50). 123789 does not meet
    these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?

Your puzzle input is 138307-654504.

--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

112233 meets these criteria because the digits never decrease and all
repeated digits are exactly two digits long. 123444 no longer meets the
criteria (the repeated 44 is part of a larger group of 444). 111122 meets
the criteria (even though 1 is repeated more than twice, it still contains
a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?

Your puzzle input is still 138307-654504.
"""

from typing import List
from runner import run


def digit(number, n_digit):
    """Return the nth digit of a given number"""
    return number // 10 ** n_digit % 10


def num_passwords1():
    """Return the number of passwords that satisfy the criteria."""
    count = 0
    for number in range(138307, 654505):
        a = digit(number, 5)
        b = digit(number, 4)
        c = digit(number, 3)
        d = digit(number, 2)
        e = digit(number, 1)
        f = digit(number, 0)
        if b < a or c < b or d < c or e < d or f < e:
            continue
        if a != b != c != d != e != f:
            continue
        count += 1
    return count


def main1():
    """Print the number of passwords."""
    print(num_passwords1())


def digits_list(number):
    """Return the digits of the given number as a list."""
    return [int(c) for c in str(number)]


def count_occurrences(ns):
    """
    Given the list of digits, return a list that for each digits contains a
    list of consecutive occurrences.
    """
    consecutive_occurrences: List[List[int]] = [
        [], [], [], [], [], [], [], [], [], []
    ]
    last_encountered = None
    for n in ns:
        occurrences = consecutive_occurrences[n]
        if last_encountered is None:
            occurrences.append(1)
        elif last_encountered == n:
            occurrences[-1] += 1
        else:
            occurrences.append(1)
        last_encountered = n
    return consecutive_occurrences


def num_passwords2():
    """Calculate the number of passwords that satisfy the criteria."""
    count = 0
    for number in range(138307, 654505):
        ns = digits_list(number)
        a, b, c, d, e, f = ns
        if b < a or c < b or d < c or e < d or f < e:
            continue
        relevant = [counts for counts in count_occurrences(ns) if 2 in counts]
        if not relevant:
            continue
        count += 1
    return count


def main2():
    """Print the number of passwords."""
    print(num_passwords2())


if __name__ == '__main__':
    run(main1, main2)
