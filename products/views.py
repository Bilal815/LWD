import json
import serpy
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail

from .serializers import ContactSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, ProductViews
from drf_extra_fields.fields import Base64ImageField
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ProductDocument
from LWD.serializers import LightSerializer, LightDictSerializer
from .search_indexes import ProductIndex


# Contact us form views inspired by https://stackoverflow.com/questions/66649074/django-rest-frame-work-send-email
# -from-contact-form
@api_view(['POST'])
def api_create_contact_view(request):
    if request.method == "POST":
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            if 'first_name' in request.POST:
                first_name = request.POST['first_name']
            else:
                first_name = "None"
            if 'email' in request.POST:
                email = request.POST['email']
            else:
                email = "None"
            if 'message' in request.POST:
                message = request.POST['message']
            else:
                message = "None"

            # send mail to the admin or the manager
            send_mail(
                'Contact Form mail from ' + first_name,
                message,
                email,
                ['test@gmail.com'],
            )
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        # To test
        # http://127.0.0.1:8000/api/contact?'first_name'="Billy"&last_name="Ash"&email="ash@gmail.com"&message="Test mail"


class CategoryListSerializer(serializers.ModelSerializer):
    # lft = serializers.SlugRelatedField(slug_field='lft', read_only=True)
    class Meta:
        model = Category
        exclude = "modified"


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = "modified"


class SerpyProductSerializer(serpy.Serializer):
    seller = serpy.StrField()
    category = serpy.StrField()
    title = serpy.StrField()
    price = serpy.FloatField()
    image = serpy.StrField()
    description = serpy.StrField()
    quantity = serpy.IntField()
    views = serpy.IntField()


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = serializers.ModelSerializer.to_representation(self, instance)
        return data


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("modified",)
        # read_only_fields = ('id', 'seller', 'category', 'title', 'price', 'image', 'description', 'quantity', 'views',)


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = "modified"


class ProductViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViews
        exclude = "modified"


class ProductDocumentSerializer(DocumentSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta(object):
        # model = Product
        document = ProductDocument
        exclude = "modified"


class ProductIndexSerializer(HaystackSerializer):
    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [ProductIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = ("text", "title", "category",)

