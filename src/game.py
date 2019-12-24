import random
from time import sleep

from faker import Faker

from config import BARRELS_NUMBER, CARDS_PER_PLAYER
from helpers import blame_numbers, clear_terminal, create_parser, hash_number_sequence

if BARRELS_NUMBER < 15:
    raise ValueError('The BARRELS_NUMBER in config.py should 15 or more')

fake = Faker()
barrels = range(1, BARRELS_NUMBER + 1)


class Player:
    players = []

    def __init__(self):
        self.cards = [Card() for _ in range(CARDS_PER_PLAYER)]
        self.is_looser = 0

    @classmethod
    def add_player_to_game(cls, player):
        cls.players.append(player)

    @classmethod
    def get_winner(cls):
        not_loosers = [player for player in cls.players if not player.is_looser]
        winners = [player for player in cls.players if player.is_winner]

        if len(not_loosers) == 1:
            return not_loosers[0]
        if winners:
            return winners[0]

    @property
    def is_winner(self):
        """True when all players cards is closed and player not marked as looser."""

        return len([card for card in self.cards if not card.is_empty]) == 0 and not self.is_looser

    def check_barrel(self, barrel: int, guess: bool):
        """Checks the player's decision to have a barrel number in his cards.

        If player have barrel number in his cards, return True if players decision is True and return False if players decision is False.
        If player doesn't have barrel number in his cards, return True if players decision is False and return False if players decision is True.
        """

        if not isinstance(guess, bool):
            raise ValueError('The decision argument should be bool value True or False')

        actually = self.check_number(barrel)

        if guess == actually and actually:
            print(f'Right! You have number {barrel} and now its marked!')  # noqa: T001
            self.mark_number(barrel)
        elif guess == actually and not actually:
            print(f'Right! You dont have number {barrel}')  # noqa: T001
        elif guess != actually and actually:
            print(f'Wrong! Actually, you have number {barrel}.')  # noqa: T001
        else:
            print(f'Wrong! Actually, you dont have number {barrel}.')  # noqa: T001

        if guess != actually:
            self.is_looser = 1

    def check_number(self, barrel: int) -> bool:
        return any([card.check_number(barrel) for card in self.cards])

    def mark_number(self, barrel: int) -> bool:
        return any([card.mark_number(barrel) for card in self.cards])

    def print_cards(self):
        for card in self.cards:
            print(card, sep='\n', end='\n')  # noqa: T001


class RobotPlayer(Player):

    def __init__(self):
        super().__init__()
        self.name = f'Robot {fake.first_name()}'

    def check_barrel(self, barrel: int) -> bool:
        guess = self.check_number(barrel)
        print(f'{self.name}, do you have number {barrel} in you cards? (y/n)')  # noqa: T001
        sleep(0.3)
        print('y' if guess else 'n')  # noqa: T001
        super().check_barrel(barrel, guess)


class HumanPlayer(Player):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def check_barrel(self, barrel: int) -> bool:
        guess_str = input(f'{self.name}, do you have number {barrel} in you cards? (y/n) ').lower()
        if guess_str not in ('y', 'n'):
            print(  # noqa: T001
                f'{guess_str} is incorrect answer. You should type only "y" or "n". Lets try again')
            self.check_barrel(barrel)
        else:
            guess = True if guess_str == 'y' else False
            super().check_barrel(barrel, guess)


class Card:
    """Lotto card class"""

    cards_in_game = set()
    number_sequences_in_game = set()

    def __init__(self):
        self._numbers = Card.get_unique_number_sequence()
        while not Card.add_card_to_game(self):
            self._numbers = random.sample(barrels, 15)

        self._numbers = blame_numbers(self._numbers)

    def __str__(self):
        str_lines = [
            ' '.join(map(str, self._numbers[:9])),
            ' '.join(map(str, self._numbers[9:18])),
            ' '.join(map(str, self._numbers[18:])),
        ]
        return '\n'.join(map(str, str_lines))

    def __hash__(self):
        return hash(tuple(sorted(self._numbers)))

    @classmethod
    def get_unique_number_sequence(cls):
        number_sequence = random.sample(barrels, 15)
        while hash_number_sequence(number_sequence) in cls.number_sequences_in_game:
            number_sequence = random.sample(barrels, 15)

        return number_sequence


    @classmethod
    def add_card_to_game(cls, card):
        if hash(card) not in cls.cards_in_game:
            cls.cards_in_game.add(hash(card))
            return True
        else:
            return False

    @property
    def numbers(self):
        return [number for number in self._numbers if isinstance(number, int)]

    @property
    def is_empty(self):
        return len(self.numbers) == 0

    def check_number(self, barrel):
        return barrel in self._numbers

    def mark_number(self, barrel):
        if self.is_empty or not self.check_number(barrel):
            return False

        self._numbers[self._numbers.index(barrel)] = 'X'
        return True


class Pouch:
    """Class fot pouch with barrels"""

    def __init__(self, barrels):
        self._barrels = list(barrels)
        random.shuffle(self._barrels)
        self._pouch_generator = (barrel for barrel in self._barrels)

    def __str__(self):
        return ' '.join(map(lambda x: str(x), self._barrels))

    def get_barrel(self):
        return next(self._pouch_generator)


class Game:

    @classmethod
    def start(cls, robot_numbers):
        clear_terminal()
        print('Welcome to the lotto game')  # noqa: T001
        human_player_name = input('What is your name? ')

        Player.add_player_to_game(HumanPlayer(human_player_name))

        for _ in range(robot_numbers):
            Player.add_player_to_game(RobotPlayer())

        pouch = Pouch(barrels=barrels)

        while True:
            barrel = pouch.get_barrel()
            clear_terminal()
            print(f'Next barrel is {barrel}')  # noqa: T001

            round_players = [player for player in Player.players if not player.is_looser]
            for player in round_players:
                clear_terminal()
                player.print_cards()
                player.check_barrel(barrel)

                if player.is_looser:
                    print('Sorry, you loose. Try again next time')  # noqa: T001
                    sleep(1)
                    break

                if player.is_winner:
                    print('Congradulationts! You win!')  # noqa: T001
                    sleep(1)
                    break

                _ = input('\nPress Enter for the next step')

            winner = Player.get_winner()
            if winner:
                clear_terminal()
                print(f'The winner is {winner.name}')  # noqa: T001
                winner.print_cards()

                break


if __name__ == '__main__':
    args = create_parser()
    Game.start(robot_numbers=args.opponents)
