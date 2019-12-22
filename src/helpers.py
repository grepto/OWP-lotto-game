from subprocess import call
from os import name
import random


def clear_terminal():
    _ = call('clear' if name == 'posix' else 'cls')


def blame_numbers(numbers):
    FILLER = ['*'] * 4
    lines = [numbers[:5] + FILLER,
             numbers[5:10] + FILLER,
             numbers[10:] + FILLER
             ]
    for line in lines:
        random.shuffle(line)

    return [item for line in lines for item in line]
