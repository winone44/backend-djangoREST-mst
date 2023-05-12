from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone



DISCOUNT_CODE_TYPES_CHOICES = [
    ('percent', 'Percentage-based'),
    ('value', 'Value-based'),
]


# Create your models here
class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class ExternalCompany(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    website = models.URLField(max_length=200)
    notes = models.TextField(blank=True, null=True)

class MyUser(AbstractBaseUser):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True,)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    credits = models.PositiveIntegerField(default=100)
    linkedin_token = models.TextField(blank=True, default='')
    expiry_date = models.DateTimeField(null=True, blank=True)
    profile_picture = models.TextField(blank=True)
    description = models.TextField(blank=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_out_of_credits(self):
        "Is the user out  of credits?"
        return self.credits > 0

    @property
    def has_sufficient_credits(self, cost):
        return self.credits - cost >= 0

    @property
    def linkedin_signed_in(self):

        return bool(self.linkedin_token) and self.expiry_date > timezone.now()

    def get_likes_count(self):
        return Like.objects.filter(video__user=self).count()

class ExternalContact(models.Model):
    person = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='person_ExternalContact')
    external_company = models.ForeignKey(ExternalCompany, on_delete=models.CASCADE, related_name='external_company')

class Friend(models.Model):
    person = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='person')
    friend = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='person_friends')


class Message(models.Model):
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'

class Video(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_video')
    title = models.CharField(max_length=100)
    video = models.TextField()
    enterprise = models.BooleanField()
    latitude_deg = models.DecimalField(max_digits=18, decimal_places=14)
    longitude_deg = models.DecimalField(max_digits=18, decimal_places=14)
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    person = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='person_who_liked')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='liked_video')

    class Meta:
        unique_together = ('person', 'video')
