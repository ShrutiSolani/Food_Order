from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import random
from datetime import date
# Create your models here.
class RestroUser(AbstractUser):
    phone_no = models.IntegerField()
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['phone_no', 'address1', 'city', 'state']


class Restaurant(models.Model):
    RId = models.AutoField(primary_key=True)
    RestroName = models.CharField(max_length=100)
    restro_phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=10)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    logo = models.URLField()
    # logo = models.ImageField(upload_to = 'restro_logo')


class Item(models.Model):
    ItemId = models.AutoField(primary_key=True)
    rId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    ItemName = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Image = models.URLField()
    # Image = models.ImageField(upload_to = 'dishes/')
    price = models.IntegerField()


class Order(models.Model):
    OrderId = models.AutoField(primary_key=True)
    uId = models.ForeignKey(RestroUser, on_delete=models.CASCADE)
    rId = models.ForeignKey(Restaurant, on_delete=models.CASCADE )
    itemId = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    odate = models.DateField(default=date.today)
    # odate = models.DateField(auto_now_add=True)
    # status_choices = [
    #     ('R','Order Received'),
    #     ('C','Cooking'),
    #     ('P','Packed and Out For Delivery'),
    #     ('D','Delivered'),
    # ]
    # status = models.CharField(max_length=5, choices=status_choices, default='R') 


class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    rId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rname = models.ForeignKey(Restaurant, to_field="RId", db_column="RestroName", on_delete=models.CASCADE, related_name="rname",default='none')
    review_given = models.CharField(max_length=250)


class Contact(models.Model):
    cId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField(max_length=250)

class OrderSummary(models.Model):
    osid = models.AutoField(primary_key=True)
    ono = models.IntegerField(unique=True, default=random.randint(100000, 999999))
    uid = models.ForeignKey(RestroUser, on_delete=models.CASCADE)
    rid = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    itemslist = models.TextField()
    total = models.IntegerField()
    status_choices = [
        ('R','Order Received'),
        ('C','Cooking'),
        ('P','Packed and Out For Delivery'),
        ('D','Delivered'),
    ]
    status = models.CharField(max_length=5, choices=status_choices, default='R') 
