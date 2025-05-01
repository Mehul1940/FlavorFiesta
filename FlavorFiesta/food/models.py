from django.db import models

# Create your models here.
class Item(models.Model):

    def __str__(self):
        return self.name  

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    ingredients = models.TextField(blank=True, null=True)  
    category = models.CharField(max_length=100, blank=True, null=True)

 