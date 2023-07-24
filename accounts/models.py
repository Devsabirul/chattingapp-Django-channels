from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="avater",
        help_text="Designates that this user has permissions to access Profile Picture.",
        verbose_name="avatar"
    )
