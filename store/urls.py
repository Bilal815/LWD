from django.urls import path
from .views import api_create_contact_view

urlpatterns = [
    path('api/contact', api_create_contact_view, name='contact'),
]