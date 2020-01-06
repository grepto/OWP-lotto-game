import pytest


@pytest.fixture
def another_barrels():
    return range(16, 31)


@pytest.fixture
def another_card(another_barrels, random_sample, random_shuffle):
    from src.game import Card
    random_sample.return_value = list(another_barrels)

    return Card(another_barrels)


@pytest.fixture
def player(player, another_card):
    player.cards.append(another_card)

    return player


@pytest.fixture
def human_player(human_player, another_card):
    human_player.cards.append(another_card)

    return human_player


@pytest.fixture
def robot_player(robot_player, another_card):
    robot_player.cards.append(another_card)

    return robot_player


@pytest.mark.parametrize('card_change, should_be_winner', [
    [lambda card: None, False],
    [lambda card: card._clear_numbers(), True],
])
def test_player_is_winner(player, card_change, should_be_winner, card,
                          another_card):
    card_change(card)
    card_change(another_card)

    assert player.is_winner == should_be_winner


@pytest.mark.parametrize('barrel, should_be_in_cards', [
    [1, True], [5, True], [16, True], [25, True], [99, False]
])
def test_player_check_number(player, barrel, should_be_in_cards):
    assert player.check_number(barrel) == should_be_in_cards


@pytest.mark.parametrize('barrel, expected_marking_result', [
    [1, True], [5, True], [16, True], [25, True], [99, False]
])
def test_player_mark_number(player, barrel, expected_marking_result):
    assert player.mark_number(barrel) == expected_marking_result


def test_robot_player_name_prefix(robot_player):
    assert robot_player.name.startswith('Robot')


@pytest.mark.parametrize('barrel, expected_answer_result', [
    [1, True], [5, True], [16, True], [25, True], [99, False]
])
def test_robot_player_get_answer(robot_player, barrel, expected_answer_result):
    assert robot_player.mark_number(barrel) == expected_answer_result


def test_human_player_name(human_player):
    assert human_player.name == 'Вольдемар'
