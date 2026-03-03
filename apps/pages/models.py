from django.db import models

# Create your models here.

class FileInfo(models.Model):
    path = models.URLField()
    info = models.CharField(max_length=255)

    def __str__(self):
        return self.path


class TechnologyChoice(models.TextChoices):
    FLOWBITE = 'FLOWBITE', 'Flowbite'
    REACT = 'REACT', 'React'
    ANGULAR = 'ANGULAR', 'Angular'
    VUE = 'VUE', 'Vue'

class DiscountChoices(models.TextChoices):
    NO = 'NO', 'No'
    FIVE = 'FIVE', '5%'
    TEN = 'TEN', '10%'
    TWENTY = 'TWENTY', '20%'
    THIRTY = 'THIRTY', '30%'
    FOURTY = 'FOURTY', '40%'
    FIFTY = 'FIFTY', '50%'

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_info = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField()
    technology = models.CharField(max_length=200, choices=TechnologyChoice.choices)
    description = models.TextField(null=True, blank=True)
    discount = models.CharField(max_length=50, choices=DiscountChoices.choices)

    def __str__(self):
        return self.name