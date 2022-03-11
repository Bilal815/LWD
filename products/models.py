from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from mptt.models import MPTTModel, TreeForeignKey
from .signals import post_signal


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


User = get_user_model()


def category_image_path(instance, filename):
    return "category/icons/{}/{}".format(instance.name, filename)


def product_image_path(instance, filename):
    return "product/images/{}/{}".format(instance.title, filename)


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to=category_image_path, blank=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(TitleSlugDescriptionModel):
    seller = models.ForeignKey(
        User, related_name="user_product", on_delete=models.CASCADE
    )
    category = TreeForeignKey(
        Category, related_name="product_category", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    image = models.ImageField(upload_to=product_image_path, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    views = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.uuid)


# @receiver(post_save, sender=Product)
# def create_index_elasticsearch(sender, instance, *args, **kwargs):
#     post_signal(sender, instance)
#     from .serializers import ProductDocumentSerializer
#     serializer = ProductDocumentSerializer(instance)
#     serializer.save()


class ProductViews(TimeStampedModel):
    ip = models.CharField(max_length=250)
    product = models.ForeignKey(
        Product, related_name="product_views", on_delete=models.CASCADE
    )
