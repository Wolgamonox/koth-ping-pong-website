from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    class Meta:
        db_table = "auth_user"

    def __str__(self) -> str:
        return f"{self.username} (pk:{self.pk})"
