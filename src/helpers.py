import argparse
import random
from os import name
from subprocess import call


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


def create_parser():
    parser = argparse.ArgumentParser(
        description='Lotto game in console'
    )
    parser.add_argument('opponents', type=int, choices=range(1, 8), default=1, help='How many opponents.')
    return parser.parse_args()
