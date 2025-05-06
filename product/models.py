from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(null=True, max_length=256)
    price = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    
class Review(models.Model):
    text = models.TextField(max_length=256)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text
    
