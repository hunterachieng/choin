from django.db import models
from django.db.models.base import Model
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


# Create your models here.
class User(AbstractUser):
    username = models.CharField(('username'), unique=False,max_length=40)
    email = models.EmailField(('email address'), unique=True)
    image = models.ImageField(upload_to='profile_image/', blank=True)
    is_previously_logged_in=models.BooleanField(default=False)
    is_superadmin = models.BooleanField(('is_superadmin'), default=False)
    is_active = models.BooleanField(('is_active'), default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    LEADERSHIP=1
    TRAINER=2
    STUDENT=3

    ROLE_CHOICES = (
        (LEADERSHIP, 'Leadership'),
        (TRAINER, 'Trainer'),
        (STUDENT, 'Student'),
    )
    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True,null=True)

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        permissions = (
            ('is_student', 'Can view student app'),
            ('is_trainer', 'Can view trainer app'),
            ('is_leader', 'Can view leader app'),
        )

    def __str__(self):
        """stirng representation"""
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Wallet(models.Model):
    owner = models.ForeignKey(User,on_delete=CASCADE, null=True)
    choinBalance = models.IntegerField(null=True,default=20)

    def __str__(self):
        return self.owner.first_name


class Metrics(models.Model):
   metric = models.CharField(max_length=100,null=True)
   value = models.IntegerField(null=True)
   date_added =models.DateTimeField(auto_now_add=True,null=True)

   def __str__(self):
        return self.metric

   def save(self):
        self.value
        super(Metrics, self).save()
        
class Transaction(models.Model):
    receiver =models.CharField(max_length = 20)
    sender =models.EmailField()
    metric = models.CharField(max_length = 100)
    value = models.IntegerField()
    time =models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.receiver

class RedeemableItem(models.Model):
    image=models.ImageField(upload_to='rewards/')
    item_name=models.CharField(max_length=50)
    item_value=models.FloatField()
    quantity=models.PositiveSmallIntegerField(default=0)
    item_in_stock=models.BooleanField(default=True)
    activate_page=models.BooleanField(default=False)

    def __str__(self) :
        return self.item_name


    

 
