from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.
class Balance(models.Model):
    balance = models.FloatField()
    address = models.CharField(max_length=100)