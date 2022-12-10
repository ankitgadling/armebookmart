from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
#import datetime
# Create your models here.
class UserEbook(models.Model):
    author=models.ForeignKey(User, default=None,on_delete=models.CASCADE )
    title=models.CharField(max_length=50)
    price=models.FloatField()
    cover=models.ImageField(upload_to="media")
    book=models.FileField(upload_to="media")
    bookaudio=models.FileField(upload_to="media")
    slug=AutoSlugField(populate_from="title", unique=True , null=True )

    def __str__(self):
        return self.title

class CartItems(models.Model):
    title =models.CharField(max_length=50,null=True)
    price=models.FloatField(null=True)

class Order(models.Model):
    ebooks = models.ForeignKey(UserEbook,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    title=models.CharField(max_length=50, default=True)

    def __str__(self):
        return self.title

class PdfToMp3(models.Model):
    book=models.FileField(upload_to="audio")
    

    
     

