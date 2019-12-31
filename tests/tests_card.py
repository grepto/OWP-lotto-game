import pytest


@pytest.fixture
def reference_hash(barrels):
    return hash(tuple(sorted(list(barrels))))


def test_card_str_magic_method(card, reference_hash):
    assert hash(card) == reference_hash


def test_card_numbers_method(card, barrels):
    assert card.numbers == list(barrels)


@pytest.mark.parametrize('card_change, should_be_empty', [
    [lambda card: None, False],
    [lambda card: card._clear_numbers(), True],
])
def test_card_is_empty(card, card_change, should_be_empty):
    card_change(card)

    assert card.is_empty == should_be_empty


@pytest.mark.parametrize('barrel, should_be_in_card', [
    [1, True], [5, True], [99, False]
])
def test_card_check_number(card, barrel, should_be_in_card):
    assert card.check_number(barrel) == should_be_in_card


@pytest.mark.parametrize('barrel, expected_marking_result', [
    [1, True], [5, True], [99, False]
])
def test_card_mark_number_removing_number(card, barrel, expected_marking_result):
    assert card.mark_number(barrel) == expected_marking_result
    assert barrel not in card.numbers


@pytest.mark.parametrize('barrel', [1, 5, 10])
def test_card_mark_number_marking_filler(card, barrel):
    filler_count_before = len([number for number in card._numbers if number == 'X'])
    card.mark_number(barrel)
    filler_count_after = len([number for number in card._numbers if number == 'X'])

    assert filler_count_after == filler_count_before + 1
