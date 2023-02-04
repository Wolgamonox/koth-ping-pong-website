from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    players = models.ManyToManyField(User)
    transitions = models.JSONField()
    date = models.DateTimeField(auto_now_add=True, editable=False)

    valid = models.BooleanField(default=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return "Game %d" % self.pk
