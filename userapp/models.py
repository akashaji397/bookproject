from django.db import models
from authenticationapp.models import UserProfile,loginTable

from bookapp.models import Book

# Create your models here.

class Cart(models.Model):

    user=models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    item=models.ManyToManyField(Book)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    
