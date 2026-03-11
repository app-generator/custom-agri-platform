import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    FARMER = 'FARMER', 'Farmer'
    ENGINEER = 'ENGINEER', 'Engineer'
    EXECUTIVE = 'EXECUTIVE', 'Executive'
    LOGISTIC = 'LOGISTIC', 'Logistic'
    AUDITOR = 'AUDITOR', 'Auditor'
    BUYER = 'BUYER', 'Buyer'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


def user_avatar_path(instance, filename):
    return os.path.join("avatar", str(instance.id), filename)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=UserRole.choices, null=True, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username