from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail

from django.utils.datastructures import MultiValueDictKeyError
from .serializers import ContactSerializer


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