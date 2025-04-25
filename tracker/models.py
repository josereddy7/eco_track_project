from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('transport', 'Transport'),
        ('food', 'Food'),
        ('electricity', 'Electricity'),
        ('shopping', 'Shopping'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    carbon_kg = models.FloatField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.carbon_kg} kg"
