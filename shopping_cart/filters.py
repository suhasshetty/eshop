from shopping_cart.models import *

from django_filters import rest_framework


class DiscountFilter(rest_framework.FilterSet):
    type = rest_framework.CharFilter(field_name="type", lookup_expr="icontains")
    valueType = rest_framework.CharFilter(field_name="value_type", lookup_expr="icontains")
    value = rest_framework.NumberFilter(field_name="value", lookup_expr="exact")
    valueFrom = rest_framework.NumberFilter(field_name="value", lookup_expr="gte")
    valueTo = rest_framework.NumberFilter(field_name="value", lookup_expr="lte")
    validFrom = rest_framework.DateFilter(field_name="valid_from", lookup_expr="exact")
    validFromStart = rest_framework.DateFilter(field_name="valid_from", lookup_expr="gte")
    validFromEnd = rest_framework.DateFilter(field_name="valid_from", lookup_expr="lte")
    validTo = rest_framework.DateFilter(field_name="valid_to", lookup_expr="exact")
    validToStart = rest_framework.DateFilter(field_name="valid_to", lookup_expr="gte")
    validToEnd = rest_framework.DateFilter(field_name="valid_to", lookup_expr="lte")

    class Meta:
        model = Discount
        fields = ["type","valueType","value","valueFrom","valueTo","validFrom",
                  "validFromStart","validFromEnd","validTo","validToStart","validToEnd"]


class ProductFilter(rest_framework.FilterSet):
    productCode = rest_framework.CharFilter(field_name="product_code", lookup_expr="icontains")
    name = rest_framework.CharFilter(field_name="name", lookup_expr="icontains")
    rating = rest_framework.NumberFilter(field_name="rating", lookup_expr="exact")
    ratingFrom = rest_framework.NumberFilter(field_name="rating", lookup_expr="gte")
    ratingTo = rest_framework.NumberFilter(field_name="rating", lookup_expr="lte")
    price = rest_framework.NumberFilter(field_name="price", lookup_expr="exact")
    priceFrom = rest_framework.NumberFilter(field_name="price", lookup_expr="gte")
    priceTo = rest_framework.NumberFilter(field_name="price", lookup_expr="lte")    
    discount = rest_framework.CharFilter(field_name="discount__discount_code", lookup_expr="icontains")
    discountedPrice = rest_framework.NumberFilter(field_name="discounted_price", lookup_expr="exact")
    discountedPriceFrom = rest_framework.NumberFilter(field_name="discounted_price", lookup_expr="gte")
    discountedPriceTo = rest_framework.NumberFilter(field_name="discounted_price", lookup_expr="lte")
    description = rest_framework.CharFilter(field_name="description", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["productCode","name","rating","ratingFrom","ratingTo","price","priceFrom","priceTo",
                  "discount","discountedPrice","discountedPriceFrom","discountedPriceTo","description"]


class ReviewFilter(rest_framework.FilterSet):
    product = rest_framework.CharFilter(field_name="product__product_code", lookup_expr="icontains")
    title = rest_framework.CharFilter(field_name="title", lookup_expr="icontains")
    description = rest_framework.CharFilter(field_name="description", lookup_expr="icontains")
    rating = rest_framework.NumberFilter(field_name="rating", lookup_expr="exact")
    ratingFrom = rest_framework.NumberFilter(field_name="rating", lookup_expr="gte")
    ratingTo = rest_framework.NumberFilter(field_name="rating", lookup_expr="lte")
    reviewer = rest_framework.CharFilter(field_name="reviewer__username", lookup_expr="icontains")
    verified = rest_framework.BooleanFilter(field_name="verified", lookup_expr="exact")

    class Meta:
        model = Review
        fields = ["product","title","description","rating","ratingFrom","ratingTo","reviewer"]


class OrderFilter(rest_framework.FilterSet):
    products = rest_framework.ModelMultipleChoiceFilter(
        field_name="products__product_code",
        to_field_name="product_code",
        queryset=Product.objects.all(),
    )
    buyer = rest_framework.CharFilter(field_name="buyer__username", lookup_expr="icontains")
    seller = rest_framework.CharFilter(field_name="seller__username", lookup_expr="icontains")
    value = rest_framework.NumberFilter(field_name="value", lookup_expr="exact")
    valueFrom = rest_framework.NumberFilter(field_name="value", lookup_expr="gte")
    valueTo = rest_framework.NumberFilter(field_name="value", lookup_expr="lte")
    status = rest_framework.CharFilter(field_name="status", lookup_expr="exact")
    created = rest_framework.DateFilter(field_name="created", lookup_expr="exact")
    createdFrom = rest_framework.DateFilter(field_name="created", lookup_expr="exact")
    createdTo = rest_framework.DateFilter(field_name="created", lookup_expr="lte")
    updated = rest_framework.DateFilter(field_name="updated", lookup_expr="exact")
    updatedFrom = rest_framework.DateFilter(field_name="updated", lookup_expr="gte")
    updatedTo = rest_framework.DateFilter(field_name="updated", lookup_expr="lte")

    class Meta:
        model = Order
        fields = ["products","buyer","seller","value","valueFrom","valueTo","status",
                  "created","createdFrom","createdTo","updated","updatedFrom","updatedTo"]


class PaymentFilter(rest_framework.FilterSet):
    order = rest_framework.NumberFilter(field_name="order__pk", lookup_expr="icontains")
    status = rest_framework.CharFilter(field_name="status", lookup_expr="exact")
    mode = rest_framework.CharFilter(field_name="mode", lookup_expr="exact")
    grossAmount = rest_framework.NumberFilter(field_name="gross_amount", lookup_expr="exact")
    grossAmountFrom = rest_framework.NumberFilter(field_name="gross_amount", lookup_expr="gte")
    grossAmountTo = rest_framework.NumberFilter(field_name="gross_amount", lookup_expr="lte")
    discount = rest_framework.CharFilter(field_name="discount__discount_code", lookup_expr="icontains")
    netAmount = rest_framework.NumberFilter(field_name="net_amount", lookup_expr="exact")
    netAmountFrom = rest_framework.NumberFilter(field_name="net_amount", lookup_expr="gte")
    netAmountTo = rest_framework.NumberFilter(field_name="net_amount", lookup_expr="lte")

    class Meta:
        model = Payment
        fields = ["order","status","mode","grossAmount","grossAmountFrom","grossAmountTo","discount",
                  "netAmount","netAmountFrom","netAmountTo"]
