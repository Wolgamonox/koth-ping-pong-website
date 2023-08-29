import datetime

import pytest
from django.utils import timezone


@pytest.mark.django_db
class TestGameEndpoints:
    endpoint = "/games/"

    def test_get_all(self, game_factory, custom_user_factory, api_client):
        # Arrange
        players = [custom_user_factory() for _ in range(3)]
        game_factory.create(players=players)

        # Act
        response = api_client().get(self.endpoint)

        # Assert
        assert response.status_code == 200

    def test_get_with_selected_players(self, game_factory, custom_user_factory, api_client):
        # Arrange
        player1 = custom_user_factory()
        player2 = custom_user_factory()
        player3 = custom_user_factory()

        game_factory.create(players=(player1, player2))
        game_factory.create(players=(player2, player3))
        game_factory.create(players=(player1, player3))

        # Act
        response_one_selected = api_client().get(self.endpoint, {"players": 1})
        response_two_selected = api_client().get(self.endpoint, {"players": [2, 3]})

        # Assert
        assert response_one_selected.status_code == 200
        assert response_one_selected.json()["count"] == 2
        assert response_two_selected.status_code == 200
        assert response_two_selected.json()["count"] == 1

    def test_get_date_before_after(self, game_factory, custom_user_factory, api_client):
        # Arrange
        players = [custom_user_factory() for _ in range(2)]
        game_factory.create(players=players, date=timezone.make_aware(datetime.datetime(2023, 8, 10)))
        game_factory.create(players=players, date=timezone.make_aware(datetime.datetime(2023, 8, 15)))
        game_factory.create(players=players, date=timezone.make_aware(datetime.datetime(2023, 8, 20)))

        # Act
        response = api_client().get(
            self.endpoint,
            {
                "date_after": timezone.make_aware(datetime.datetime(2023, 8, 11)),
                "date_before": timezone.make_aware(datetime.datetime(2023, 8, 19)),
            },
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_get_single_game(self, game_factory, custom_user_factory, api_client):
        # Arrange
        players = [custom_user_factory() for _ in range(3)]
        game_factory.create(players=players)
        game2 = game_factory.create(players=players[:2])

        # Act
        response = api_client().get(f"{self.endpoint}{game2.pk}/")

        # Assert
        assert response.status_code == 200
        assert len(response.json()["players"]) == 2

    # TODO post test
