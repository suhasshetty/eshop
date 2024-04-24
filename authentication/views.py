"""Api file for handling authentications."""

from django.contrib.auth.hashers import make_password

from authentication.models import *
from authentication.filters import *
from authentication.serializers import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView



# Create your views here.
class RegisterView(APIView):
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def post(self, request):
        users_by_email = users_by_phone_number = None
        email = request.data.get("email", None)
        phone_number = request.data.get("phone_number", None)
        users_by_email = User.objects.filter(email=email)
        users_by_phone_number = User.objects.filter(phone_number=phone_number)
        if users_by_email and users_by_phone_number:
            raise serializers.ValidationError(f"A user with that email-id and phone number already exists.")
        elif users_by_email:
            raise serializers.ValidationError(f"A user with that email-id already exists.")
        elif users_by_phone_number:
            raise serializers.ValidationError(f"A user with that phone number already exists.")
        else:
            password = request.data.get("password", None)
            if password:
                request.data["password"] = make_password(password)
            elif users_by_phone_number:
                raise serializers.ValidationError(f"A user without password cannot exist.")
            register_serializer = UserSerializer(data=request.data)
            register_serializer.is_valid(raise_exception=True)
            register_serializer.save()
            return Response(register_serializer.data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def create(self, request, *args, **kwargs):
        users_by_email = users_by_phone_number = None
        email = request.data.get("email", None)
        phone_number = request.data.get("phone_number", None)
        users_by_email = User.objects.filter(email=email)
        users_by_phone_number = User.objects.filter(phone_number=phone_number)
        if users_by_email and users_by_phone_number:
            raise serializers.ValidationError(f"A user with that email-id and phone number already exists.")
        elif users_by_email:
            raise serializers.ValidationError(f"A user with that email-id already exists.")
        elif users_by_phone_number:
            raise serializers.ValidationError(f"A user with that phone number already exists.")
        else:
            return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        users_by_email = users_by_phone_number = None
        username = request.data.get("username", None)
        user = User.objects.filter(username=username).first()
        if user:
            raise serializers.ValidationError(f"A user with that username already exists.")
        else:
            return viewsets.ModelViewSet.update(self, request, *args, **kwargs)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
