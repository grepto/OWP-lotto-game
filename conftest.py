import pytest

from src.game import HumanPlayer, RobotPlayer, Player, Card


@pytest.fixture
def blame_numbers(mocker):
    return mocker.patch('src.helpers.blame_numbers')


@pytest.fixture
def random_shuffle(mocker):
    return mocker.patch('random.shuffle')


@pytest.fixture
def random_sample(mocker):
    return mocker.patch('random.sample')


@pytest.fixture
def barrels():
    return range(1, 16)


@pytest.fixture
def card(barrels, random_sample, random_shuffle):
    random_sample.return_value = list(barrels)

    return Card(barrels)


@pytest.fixture
def player(card):
    player = Player()
    player.cards.append(card)

    return player


@pytest.fixture
def human_player(card):
    player = HumanPlayer('Вольдемар')
    player.cards.append(card)

    return player


@pytest.fixture
def robot_player(card):
    player = RobotPlayer()
    player.cards.append(card)

    return player
