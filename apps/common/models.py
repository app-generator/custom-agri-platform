from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Farm(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Parcel(BaseModel):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    polygon = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class CropType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Substance(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CropPlan(BaseModel):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='crop_plans')
    crop_type = models.ForeignKey(CropType, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.crop_type} {self.year}"


class ParcelAction(BaseModel):

    ACTION_TYPES = (
        ("SPRINKLE", "Sprinkling"),
        ("HARVEST", "Harvest"),
    )

    crop_plan = models.ForeignKey(CropPlan, on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)

    substance = models.ForeignKey(
        Substance,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date = models.DateField()

    def __str__(self):
        return f"{self.action_type} - {self.date}"