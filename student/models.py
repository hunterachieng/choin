from django.db import models
from django.contrib.auth.models import AbstractUser
from leadership.models import User , Wallet
from django.db.models.deletion import CASCADE, SET_NULL
from django.dispatch import receiver
from django.db.models.signals import post_save
from leadership.models import RedeemableItem
# Create your models here.

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=CASCADE,null=True,related_name='userprofile')
    class_name = models.CharField(max_length=20, blank=True)
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role==3:
            Student.objects.create(user=instance)
            Wallet.objects.create(owner=instance)
    else:
        pass

class Redeem(models.Model):
    # cart
    #order
   
    student=models.ForeignKey(Student,on_delete=CASCADE,null=True)
    date_of_purchase=models.DateField(null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    @property
    def calculate_cart_total(self):
        orderitems=self.rewardeditem_set.all()
        total_price=sum([item.calculate_total for item in orderitems])
        return total_price
    
    @property
    def calculate_cart_items(self):
        orderitems=self.rewardeditem_set.all()
        total_items=sum([item.quantity for item in orderitems])
        return total_items

class RewardedItem(models.Model):
    # item within the cart
    reward=models.ForeignKey(RedeemableItem,on_delete=CASCADE, null=True,blank=False)
    order=models.ForeignKey(Redeem,on_delete=CASCADE ,null=True,blank=False)
    quantity=models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def calculate_total(self):
        total_price=self.reward.item_value * self.quantity
        return total_price
class Redeemed(models.Model):
    product = models.ForeignKey(RedeemableItem,on_delete=CASCADE, null=True,blank=False)
    quantity = models.IntegerField(default=0)
    total =  models.IntegerField(default=0)
    student = models.ForeignKey(Student,on_delete=CASCADE,null=True)
    date = models.DateField(auto_now_add=True,null=True)
