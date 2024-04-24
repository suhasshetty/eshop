from shopping_cart.models import *

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [field.name for field in model._meta.fields]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [field.name for field in model._meta.fields]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [field.name for field in model._meta.fields]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [field.name for field in model._meta.fields]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [field.name for field in model._meta.fields]
