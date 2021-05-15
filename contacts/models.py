from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)




class UserContacts(models.Model):
    customer = models.ForeignKey(Customer,blank=True,on_delete=models.CASCADE,null=True)
    full_name = models.CharField(max_length=250,null=True)
    relationship = models.CharField(max_length=250,null=True)
    email = models.EmailField(max_length=254,blank=True)
    phone_number = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=1000,blank=True)

    def __str__(self):
          return self.full_name