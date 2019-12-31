import pytest


def test_pouch_getting_barrels(pouch, barrels):
    for barrel in barrels:
        assert pouch.get_new_barrel() == barrel
