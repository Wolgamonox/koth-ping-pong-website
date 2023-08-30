import random

import factory
from accounts.models import CustomUser
from django.utils import timezone
from games.models import Game


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"robert{n}")
    first_name = "Robert"
    last_name = "Ravioli"


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    date = factory.LazyFunction(timezone.now)

    # Initialize the transitions with dummy list, it will be filled later
    transitions = [{"player": 1, "duration": 1}]

    @factory.post_generation
    def players(self, create, new_players, **kwargs):
        if not create or not new_players:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of new_players using bulk addition
        self.players.add(*new_players)

        # build the transitions here, havent found a better way
        duration = None
        if "transition_duration" in kwargs:
            duration = kwargs["transition_duration"]

        self.transitions = [
            {
                "player": random.choice(self.players.all()).pk,
                "duration": duration if duration else random.randint(1, 100),
            }
            for _ in range(10)
        ]
