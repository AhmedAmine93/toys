from django.db import models

class Toy(models.Model):
   name = models.CharField(max_length=100)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   description = models.TextField()
   image_url = models.URLField()
   age_restriction = models.CharField(max_length=10, choices=(
       ('3+', '3+'), ('6+', '6+'), ('8-12', '8-12'), ('16', '16'), ('18+', '18+')
   ))

class ToyVariant(models.Model):
   toy = models.ForeignKey(Toy, on_delete=models.CASCADE)
   color = models.CharField(max_length=50)
   support_type = models.CharField(max_length=50)

# Create your models here.
