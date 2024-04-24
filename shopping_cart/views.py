from datetime import datetime, timezone

from shopping_cart.filters import *
from shopping_cart.models import *
from shopping_cart.serializers import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = DiscountSerializer
    filterset_class = DiscountFilter

    def create(self, request, *args, **kwargs):
        discount = None
        discount_code = request.data.get("discount_code", None)
        discount = Discount.objects.filter(discount_code=discount_code)
        if discount:
            raise serializers.ValidationError(f"A discount with that discount code already exists.")
        else:
            return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        discount_code = request.data.get("discount_code", None)
        discount_by_code = Discount.objects.filter(discount_code=discount_code)
        id = kwargs["pk"]
        discount_by_id = Product.objects.filter(id=id).first()
        if discount_by_code:
            raise serializers.ValidationError(f"A discount with that discount code already exists.")
        elif discount_by_id:
            return viewsets.ModelViewSet.update(self, request, *args, **kwargs)
        else:
            raise serializers.ValidationError(f"A discount of the id does not exist.")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def create(self, request, *args, **kwargs):
        discount_value = discount_amount = discounted_price = price = 0
        product_code = request.data.get("product_code", None)
        products = Product.objects.filter(product_code=product_code)
        if products:
            raise serializers.ValidationError(f"A product with that product code already exists.")
        else:
            discounted_price = price = request.data.get("price", None)
            discount_id = request.data.get("discount", None)
            if discount_id:
                today = datetime.now(tz=timezone.utc)
                discount_obj = Discount.objects.filter(id=discount_id, valid_from__lte=today, valid_to__gte=today).first()
                if discount_obj:
                    discount_value = discount_obj.value
                    discount_value_type = discount_obj.value_type
                    if discount_value_type == DiscountValueTypes.FIXED.value:
                        discounted_price = price - discount_value
                    elif discount_value_type == DiscountValueTypes.PERCENTAGE.value:
                        discount_amount = (price * discount_value)/100
                        discounted_price = price - discount_amount
            request.data["discounted_price"] = discounted_price
            return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        discount_value = discount_amount = discounted_price = price = 0
        id = kwargs["pk"]
        product_code = request.data.get("product_code", None)
        product_by_product_code = Product.objects.filter(product_code=product_code).first()
        product_by_id = Product.objects.filter(id=id).first()
        if product_by_product_code:
            raise serializers.ValidationError(f"A product with that product code already exists.")
        elif product_by_id:
            price = request.data.get("price", product_by_id.price)
            discount_id = request.data.get("discount", None)
            if discount_id:
                today = datetime.now(tz=timezone.utc)
                discount_obj = Discount.objects.filter(id=discount_id, valid_from__lte=today, valid_to__gte=today).first()
                if discount_obj:
                    discount_value = discount_obj.value
                    discount_value_type = discount_obj.value_type
                    if discount_value_type == DiscountValueTypes.FIXED.value:
                        discounted_price = price - discount_value
                    elif discount_value_type == DiscountValueTypes.PERCENTAGE.value:
                        discount_amount = (price * discount_value)/100
                        discounted_price = price - discount_amount
                    request.data["discounted_price"] = discounted_price
            return viewsets.ModelViewSet.update(self, request, *args, **kwargs)
        else:
            raise serializers.ValidationError(f"A product of the id does not exist.")


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product", None)
        reviewer_id = request.data.get("reviewer", None)
        rating = request.data.get("rating", None)
        if product_id and reviewer_id and rating:
            product = Product.objects.filter(id=product_id).first()
            reviewer = User.objects.filter(id=reviewer_id).first()
            existing_review = Review.objects.filter(product=product, reviewer=reviewer).first()
            if product:
                if reviewer:
                    if existing_review:
                        raise serializers.ValidationError(f"A review with that product and reviewer already exists.")
                    else:
                        average_rating_from_db = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
                        average_rating = average_rating_from_db if average_rating_from_db else 0
                        product.rating = (average_rating + rating)/2
                        product.save()
                        order = Order.objects.filter(products__id=product_id, buyer=reviewer)
                        if order:
                            request.data["verified"] = True
                        else:
                            request.data["verified"] = False
                        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
                else:
                    raise serializers.ValidationError(f"A user of the id does not exist.")
            else:
                raise serializers.ValidationError(f"A product of the id does not exist.")
        else:
            raise serializers.ValidationError(f"A review without product, reviewer and rating cannot exist.")

    def update(self, request, *args, **kwargs):
        product_id = request.data.get("product", None)
        reviewer_id = request.data.get("reviewer", None)
        rating = request.data.get("rating", None)
        if product_id and reviewer_id and rating:
            product = Product.objects.filter(id=product_id).first()
            reviewer = User.objects.filter(id=reviewer_id).first()
            existing_review = Review.objects.filter(product=product, reviewer=reviewer).first()
            if product:
                if reviewer:
                    if existing_review:
                        raise serializers.ValidationError(f"A review with that product and reviewer already exists.")
                    else:
                        average_rating_from_db = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
                        average_rating = average_rating_from_db if average_rating_from_db else 0
                        product.rating = (average_rating + rating)/2
                        product.save()
                        order = Order.objects.filter(products__id=product_id, buyer=reviewer)
                        if order:
                            request.data["verified"] = True
                        else:
                            request.data["verified"] = False
                        return viewsets.ModelViewSet.update(self, request, *args, **kwargs)
                else:
                    raise serializers.ValidationError(f"A user of the id does not exist.")
            else:
                raise serializers.ValidationError(f"A product of the id does not exist.")
        else:
            raise serializers.ValidationError(f"A review without product, reviewer and rating cannot exist.")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = OrderSerializer
    filterset_class = OrderFilter

    def create(self, request, *args, **kwargs):
        value = 0
        product_ids = request.data.get("products", None)
        for id in product_ids:
            product = Product.objects.filter(id=id).first()
            value = value + product.discounted_price
        request.data["value"] = value
        status = OrderStatus.PLACED.value
        request.data["status"] = status
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        value = 0
        id = kwargs["pk"]
        order = Order.objects.filter(id=id).first()
        product_ids = request.data.get("products", None)
        for id in product_ids:
            product = Product.objects.filter(id=id).first()
            value = value + product.discounted_price
        request.data["value"] = value
        if order:
            status = request.data.get("status", order.status)
        else:
            raise serializers.ValidationError(f"An order of the id does not exist.")
        request.data["status"] = status
        return viewsets.ModelViewSet.update(self, request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter

    def create(self, request, *args, **kwargs):
        discount_value = 0
        mode = request.data.get("mode", None)
        order_id = request.data.get("order", None)
        if order_id:
            order = Order.objects.filter(id=order_id).first()
            if order:
                net_amount = gross_amount = order.value
                discount_id = request.data.get("discount", None)
                if discount_id:
                    discount = Discount.objects.filter(id=discount_id).first()
                    if discount:
                        discount_mode = discount.mode if discount.mode else None
                        if discount_mode and discount_mode == mode:
                            discount_value = discount.value
                        elif discount_mode == None:
                            discount_value = discount.value
                        net_amount = gross_amount - discount_value
                        request.data["gross_amount"] = gross_amount
                        request.data["net_amount"] = net_amount
                        status = PaymentStatus.PENDING.value
                        request.data["status"] = status
                return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
            else:
                raise serializers.ValidationError(f"An order of the order id does not exist.")
        else:
            raise serializers.ValidationError(f"A payment without order cannot exist.")


    def update(self, request, *args, **kwargs):
        id = kwargs["pk"]
        payment = Payment.objects.filter(id=id).first()
        if payment:
            status = request.data.get("status", payment.status)
        else:
            raise serializers.ValidationError(f"A payment of the id does not exist.")
        order_id = payment.order_id
        order = Order.objects.filter(id=order_id).first()
        if order_id:
            order = Order.objects.filter(id=order_id).first()
            if order:
                request.data["status"] = status
                request.data["order"] = order_id
                return viewsets.ModelViewSet.update(self, request, *args, **kwargs)
            else:
                raise serializers.ValidationError(f"An order of the order id does not exist.")
        else:
            raise serializers.ValidationError(f"A payment without order cannot exist.")
