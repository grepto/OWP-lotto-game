import pytest

from src.game import Pouch


@pytest.fixture
def pouch(barrels, random_shuffle):
    return Pouch(barrels)


def test_pouch_getting_barrels(pouch, barrels):
    for barrel in barrels:
        assert pouch.get_new_barrel() == barrel
