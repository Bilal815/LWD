from .models import BlogPage
from rest_framework import viewsets
from .serializers import BlogSerializer


# Blog Viewset
class BlogViewSet(viewsets.ModelViewSet):
    queryset = BlogPage.objects.all()
    serializer_class = BlogSerializer
