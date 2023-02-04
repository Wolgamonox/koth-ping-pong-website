import datetime

import factory
from django.contrib.auth.models import User
from games.models import Game


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    password = "test"
    username = "Bob"
    is_superuser = False
    is_staff = False


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    transitions = {}
    date = datetime.datetime(2007, 2, 4, 12, 34, 15)

    valid = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.groups.add(*extracted)
