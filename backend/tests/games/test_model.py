import pytest


@pytest.mark.django_db
class TestGameModel:
    def test_total_duration(self, game_factory, custom_user_factory):
        # Arrange
        players = [custom_user_factory() for _ in range(3)]

        # Act
        game = game_factory.create(players=players, players__transition_duration=10)

        # Assert
        assert game.total_duration == 10 * 10
