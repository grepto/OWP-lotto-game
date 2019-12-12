import argparse
import random
import time

BARRELS = range(1, 91)


class Card:
    """Lotto card class"""

    def __init__(self, name):
        self.name = name
        self._numbers = random.sample(BARRELS, 14)

    def __str__(self):
        return self.name

    def get_numbers(self):
        return self._numbers

    def check_number(self, barrel):
        if barrel in self._numbers:
            self._numbers.remove(barrel)
            return True
        return False

    def is_winner(self):
        return len(self._numbers) == 0


class Pouch:
    """Class fot pouch with barrels"""

    def __init__(self):
        self._barrels = list(BARRELS)

    def __str__(self):
        return self._barrels

    def get_barrel(self):
        barrel = random.choice(self._barrels)
        self._barrels.remove(barrel)
        return barrel

    def is_empty(self):
        return len(self._barrels) == 0


def create_cards(number_of_cards):
    return [Card(f'Player {number}') for number in range(1, number_of_cards + 1)]


def check_cards_number(cards, barrel):
    return [card for card in cards if card.check_number(barrel)]


def get_winners(cards):
    return [card for card in cards if card.is_winner()]


def create_parser():
    parser = argparse.ArgumentParser(
        description='Lotto game in console'
    )
    parser.add_argument('players', type=int, choices=range(1, 8), default=2, help='How many players.')
    return parser.parse_args()


def app(players):
    pouch = Pouch()
    cards = create_cards(players)

    while not pouch.is_empty():
        for card in cards:
            print(card, card.get_numbers())

        barrel = pouch.get_barrel()
        print('Next barrel is', barrel)
        cards_with_number = ','.join([card.name for card in check_cards_number(cards, barrel)])
        print(f'Cards {cards_with_number} has number {barrel}' if cards_with_number else f'No one has number {barrel}',
              end='\n\n')

        if get_winners(cards):
            break

        time.sleep(0.5)

    winners = get_winners(cards)
    print(f'The {"winners" if len(winners) > 1 else "winner"} is', *winners)


if __name__ == '__main__':
    parser = create_parser()
    app(players=parser.players)
