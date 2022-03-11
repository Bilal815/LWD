from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class User(models.Model):
    """All the data when a user signs up as a customer"""
    user = models.OneToOneField(User, related_name='userprofile', default=0, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    picture = models.ImageField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True,
                                    blank=True)  # validators should be a list
    address = models.CharField(max_length=95, unique=True)

    session_token = models.CharField(max_length=35, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '%s' % self.user.username

User.userprofile = property(lambda u:User.objects.get_or_create(user=u)[0])