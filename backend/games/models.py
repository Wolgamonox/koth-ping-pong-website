from accounts.models import CustomUser
from django.db import models
from django.utils import timezone



class Game(models.Model):
    players = models.ManyToManyField(CustomUser)
    transitions = models.JSONField()
    date = models.DateTimeField(default=timezone.now, editable=False)

    valid = models.BooleanField(default=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"Game [{self.pk}]"