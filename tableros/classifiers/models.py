from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.title}"
    
class Sentiment(models.Model):
    Gender_choices =(
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
    )
    
    Country_choices = (
        ("USA", "USA"),
        ("Canada", "Canada"),
        ("México", "México"),
        ("Europa", "Europa"),
        ("Japón", "Japón"),
        ("Corea del Sur", "Corea del Sur")
    )
    
    movie     = models.ForeignKey(Movie, on_delete=models.CASCADE)
    reviews   = models.TextField()
    results   = models.IntegerField()
    gender    = models.CharField(max_length=9, choices=Gender_choices)
    age       = models.IntegerField()
    country   = models.CharField(max_length=24, choices=Country_choices)
    timestamp = models.DateField(auto_now_add=True)
    updated   = models.DateField(auto_now=True)
    
    