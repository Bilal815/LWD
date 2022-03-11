from django.contrib import admin
from .models import ContactForm, Category, Product

# Register your models here.
admin.site.register(ContactForm)
admin.site.register(Category)
admin.site.register(Product)