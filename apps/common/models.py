from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Parcel(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    polygon = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)