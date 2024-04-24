from django.urls import include, path

from shopping_cart.views import *

from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)

router.register(r"discounts", DiscountViewSet, basename="dsicounts")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
