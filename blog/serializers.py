from rest_framework import serializers
from .models import BlogPage

# User Serializer
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPage
        fields = '__all__'
        ordering = ['date_added']

