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



#

class Sheet(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Tab(BaseModel):
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class FieldType(models.TextChoices):
    STRING = "STRING", "String"
    NUMERIC = "NUMERIC", "Numeric"
    DATE = "DATE", "Date"

class TabFields(BaseModel):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=30, choices=FieldType.choices)

    def __str__(self):
        return self.name
    
    
class TabRow(BaseModel):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, related_name="rows")
    row_index = models.IntegerField()

    def __str__(self):
        return f"{self.tab.name} - Row {self.row_index}"


class TabCell(BaseModel):
    row = models.ForeignKey(TabRow, on_delete=models.CASCADE, related_name="cells")
    field = models.ForeignKey(TabFields, on_delete=models.CASCADE)
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.field.name}: {self.value}"


class Asset(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.ForeignKey(TabRow, on_delete=models.CASCADE)
    file = models.FileField(upload_to='asset')

    @property
    def filename(self):
        return self.file.name