from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class ContactForm(models.Model):
    """Contact Form Model"""
    serial_no = models.AutoField(primary_key=True)
    first_name = models.CharField(verbose_name='first_name', max_length=255, unique=False)
    last_name = models.CharField(verbose_name='first_name', max_length=255, unique=False)
    email = models.EmailField(max_length=100, unique=False)
    message = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True,
                                    blank=True)  # validators should be a list
    timestamp = models.DateTimeField(auto_now_add=True)