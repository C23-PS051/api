from django.db import models
from django.contrib.auth.models import User

class Cafe(models.Model):
    data = models.JSONField()

    def __str__(self):
        return self.data