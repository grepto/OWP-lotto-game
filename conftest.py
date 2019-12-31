import pytest

from src.game import HumanPlayer, RobotPlayer, Pouch, Card


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
def human_player():
    return HumanPlayer('Вольдемар')


@pytest.fixture
def robot_player():
    return RobotPlayer()


@pytest.fixture
def barrels():
    return range(1, 16)


@pytest.fixture
def pouch(barrels, random_shuffle):
    return Pouch(barrels)


@pytest.fixture
def card(barrels, random_sample, random_shuffle):
    random_sample.return_value = list(barrels)

    return Card(barrels)
