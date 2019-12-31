import pytest

from src.game import Card, Game, HumanPlayer, RobotPlayer


@pytest.fixture
def game(robot_player, human_player):
    game = Game(15, 2, 1)
    game.players = [robot_player, human_player]

    return game


@pytest.fixture
def human_is_winner(mocker):
    return mocker.patch('src.game.HumanPlayer.is_winner')


def test_game_init(game):
    assert game.cards_per_player == 2
    assert game.robots_number == 1
    assert len(game.pouch.barrels) == 15


def test_add_card(game):
    assert isinstance(game.add_card(), Card)


def test_add_player(game):
    assert isinstance(game.add_player(), RobotPlayer)
    assert isinstance(game.add_player('Пепяка'), HumanPlayer)


def test_deal_cards_to_players(game, human_player, robot_player):
    game.deal_cards_to_players()

    assert len(robot_player.cards) == 2
    assert len(human_player.cards) == 2


def test_get_winner_through_looser(game, human_player, robot_player):
    human_player.is_looser = True

    assert game.get_winner() == robot_player


def test_get_winner_through_winner(game, human_player, human_is_winner):
    human_is_winner.return_value = True

    assert game.get_winner() == human_player
