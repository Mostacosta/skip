from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid
import string
import random

# Create your models here.

class UserManager(BaseUserManager):
    """
    class manager for providing a User(AbstractBaseUser) full control
    on this objects to create all types of User and this roles.
    """
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """
        pass data  to '_create_user' for creating normal_user .
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """
        pass data to '_create_user' for creating super_user .
        """
        if phone is None:
            raise TypeError('Users must have an phone address.')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    individual,buisness = "1","2"
    user_types = [(individual,"individual"),(buisness,"buisness")]

    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    email = models.EmailField(db_index=True, unique=True,blank=True,null=True)
    full_name = models.CharField(max_length=500,blank=True,null=True)
    phone = models.CharField(max_length=50, unique=True)
    user_type = models.CharField(choices=user_types,max_length=1,default=individual)
    image = models.ImageField(upload_to="profile_pic",blank=True,null=True)
    finger_print = models.CharField(max_length=200,blank=True,null=True,unique=True)
    friends = models.ManyToManyField('self',blank=True,null=True)
    balance = models.FloatField(default=0.0)
    is_verify = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    static_qr = models.ImageField(upload_to="qrcode",null=True,blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name',]

    objects = UserManager()

    def __str__(self):
        return self.phone

    def check_balance(self,amount):
        if float(amount) <= self.balance:
            return True
        return False



def code_generator(size=4, chars=string.ascii_letters + string.digits):
    code = "".join(random.choice(chars) for _ in range(size))
    check = Code.objects.filter(code=code)
    if check.exists():
        return code_generator()
    else:
        return code

class Code (models.Model):
    code = models.CharField(max_length=4, unique=True)
    phone = models.CharField(max_length=12)
    verify = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs) -> None:
        self.code = code_generator()
        return super().save(*args, **kwargs)


class Version(models.Model):
    version = models.CharField(max_length=30, unique=True)
    status = models.BooleanField(default=True)

class PaymentRequest(models.Model):

    pay,request = "1","2"
    accept,reject,pending = "1","2","3"

    TYPES = [(pay,"pay"),(request,"request")]
    RESPONSE_TYPES = [(accept,"accept"),(reject,"reject"),(pending,"pending")]

    sender = models.ForeignKey("User",on_delete=models.CASCADE,related_name="senderuser")
    receiver = models.ForeignKey("User",on_delete=models.CASCADE,related_name="receiveruser")
    note = models.TextField(blank=True,null=True)
    amount = models.FloatField()
    type = models.CharField(max_length=1,choices=TYPES)
    response = models.CharField(max_length=1,choices=RESPONSE_TYPES,default=pending)

class Notfication(models.Model):
    receiver = models.ForeignKey("User",on_delete=models.CASCADE,related_name="notireceiver")
    request = models.ForeignKey("PaymentRequest",on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

