""" --- Part Two ---

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


def digits(number):
    """Return the digits of the given number as a list."""
    return [int(c) for c in str(number)]


def count_occurrences(ns):
    """
    Given the list of digits, return a list that for each digits contains a
    list of consecutive occurrences.
    """
    consecutive_occurrences = [
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


def num_passwords():
    """Calculate the number of passwords that satisfy the criteria."""
    count = 0
    for number in range(138307, 654505):
        ns = digits(number)
        a, b, c, d, e, f = ns
        if b < a or c < b or d < c or e < d or f < e:
            continue
        relevant = [counts for counts in count_occurrences(ns) if 2 in counts]
        if not relevant:
            continue
        count += 1
    return count


if __name__ == '__main__':
    print(num_passwords())
