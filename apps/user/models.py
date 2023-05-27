import email
from itertools import product
import profile
from tokenize import group
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import Group
from django.db import transaction

class Role(models.Model):
    """
    User roles
    1 - ADMIN
    2 - USER

    Args:
        models (_type_):user roles
    """
    role_name = models.CharField(max_length=256)
    is_active = models.BooleanField(default= True)
    class Meta:
        db_table = 'social_role_master'

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise Exception('Model creation Error')

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)

class Profile(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=60,null=True)
    profile_picture = models.CharField(null=True,max_length=256)
    role = models.ForeignKey(Role, related_name='+', on_delete=models.CASCADE,null=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)   
    last_login = models.DateTimeField(blank=True,null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
      db_table = 'social_auth_users'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        return self
    
class FriendRequest(models.Model):

    """
    status:
    
    REQUESTED
    ACCEPTED
    REJECTED
    """
     
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    status = models.CharField(max_length=10, null = False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)

    class Meta:
      db_table = 'social_friend_request' 

class Friend(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True) 

    class Meta:
      db_table = 'social_friend'

