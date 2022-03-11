from rest_framework import serializers
from .models import ContactForm


class ContactSerializer(serializers.ModelSerializer):
    """Contact form serializer"""
    class Meta:
        model = ContactForm
        fields = ('first_name', 'last_name', 'email', 'message', 'phone')

    def contact(self):
        form = self.POST
        form.save(commit=False)
        form.save()

