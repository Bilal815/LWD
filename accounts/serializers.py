from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from .forms import SignUpForm, UserprofileForm

# User Serializer inspired by https://github.com/bradtraversy/lead_manager_react_django
@login_required
@api_view(['GET'])
class UserSerializer(serializers.ModelSerializer):
    """User profile data for registered user, after login"""
    class Meta:
        model = User
        fields = ('username', 'email', 'picture')


# Register Serializer  inspired by https://github.com/SteinOveHelset/saulgadgets
class RegisterSerializer(serializers.ModelSerializer):
    """Register accounts for new accounts"""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        extra_kwargs = {'password1': {'write_only': True}, 'password2': {'write_only': True}, 'email': {'write_only': True}}

    @api_view(['POST'])
    def signup(self, request, validated_data):

      if request.method == 'POST':
        form = SignUpForm(request.POST)
        userprofileform = UserprofileForm(request.POST)

        if form.is_valid() and userprofileform.is_valid():
            user = form.save()

            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            userprofile.save()

            user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            login(request, user)
            return user
        raise serializers.ValidationError("Fields Missing!")


# Login Serializer inspired by https://github.com/bradtraversy/lead_manager_react_django
class LoginSerializer(serializers.Serializer):
    """Login registered users"""


    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")