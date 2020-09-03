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
"""


def digit(number, n):
    """Return the nth digit of a given number"""
    return number // 10**n % 10


def num_passwords():
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


if __name__ == '__main__':
    print(num_passwords())
