from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1000)
    price = models.FloatField()
    tags = models.ManyToManyField(Tag)
    stock = models.IntegerField()

    def __str__(self):
        return self.name
    
class Request(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Tag)
    date = models.DateField()
    price_range = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartProduct')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.cart.user.username

    
class List(models.Model):
    products = models.ManyToManyField(Product, through='ListProduct')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    
class ListProduct(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.list.user.username




