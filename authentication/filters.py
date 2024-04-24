from authentication.models import *

from django_filters import rest_framework


class UserFilter(rest_framework.FilterSet):
    username = rest_framework.CharFilter(field_name="username", lookup_expr="icontains")
    firstName = rest_framework.CharFilter(field_name="first_name", lookup_expr="icontains")
    lastName = rest_framework.CharFilter(field_name="last_name", lookup_expr="icontains")
    displayName = rest_framework.CharFilter(field_name="display_name", lookup_expr="icontains")
    email = rest_framework.CharFilter(field_name="email", lookup_expr="icontains")
    dateOfBirth = rest_framework.DateFilter(field_name="date_of_birth", lookup_expr="exact")
    dateOfBirthFrom = rest_framework.DateFilter(field_name="date_of_birth", lookup_expr="gte")
    dateOfBirthTo = rest_framework.DateFilter(field_name="date_of_birth", lookup_expr="lte")
    gender = rest_framework.CharFilter(field_name="gender", lookup_expr="exact")
    phoneNumber = rest_framework.NumberFilter(field_name="phone_number", lookup_expr="icontains")
    address = rest_framework.CharFilter(field_name="address", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ["username","firstName","lastName","displayName","email","dateOfBirth",
                  "dateOfBirthFrom","dateOfBirthTo","gender","phoneNumber","address"]
