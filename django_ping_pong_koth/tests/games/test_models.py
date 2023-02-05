import pytest

pytestmark = pytest.mark.django_db


class TestGameModel:
    def test_str_return(self, game_factory):
        game = game_factory()

        assert game.__str__() == "Game %s" % game.date.strftime("%Y-%m-%d %H:%M:%S")