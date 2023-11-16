
from django.db import models

class Review(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=10, blank=True, null=True)

class Brands(models.Model):
    id=models.IntegerField(primary_key=True)
    Name=models.CharField(max_length=100)
    Avg_Polarity=models.DecimalField(max_digits=5,decimal_places=2,default=0.0)
    Avg_Subjectivity=models.DecimalField(max_digits=5,decimal_places=2,default=0.0)
    Recent_Comments=models.CharField(max_length=1000)
    Number_of_Reviews=models.IntegerField(null=False,default=0)

class Reviews(models.Model):
    name=models.CharField(max_length=100)
    text = models.TextField()
    sentiment = models.CharField(max_length=10, blank=True, null=True)