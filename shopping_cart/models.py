from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import *
from django.utils import timezone
from enum import Enum

from authentication.models import User

from simple_history import register


# Create your models here.
class DiscountTypes(str, Enum):
    SELLER_COUPON = "seller_coupon"
    SELLER_OFFER = "seller_offer"
    PLATFORM_COUPON = "platform_coupon"
    PLATFORM_OFFER = "platform_offer"
    PAYMENT_MODE_COUPON = "payment_mode_coupon"
    PAYMENT_MODE_OFFER = "payment_mode_offer"

    @classmethod
    def choices(obj):
        return tuple((item.value, item.name) for item in obj)
    
class DiscountValueTypes(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"

    @classmethod
    def choices(obj):
        return tuple((item.value, item.name) for item in obj)


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

    @classmethod
    def choices(obj):
        return tuple((item.value, item.name) for item in obj)


class PaymentModes(str, Enum):
    CASH = "cash"
    DEBIT_CARD = "debit"
    CREDIT_CARD = "credit"
    UPI = "upi"
    NET_BANKING = "net_banking"
    EMI_DEBIT_CARD = "emi_debit"
    EMI_CREDIT_CARD = "emi_credit"
    PAY_LATER = "later"
    WALLET_INHOUSE = "wallet"
    WALLET_THIRD_PARTY = "wallet_external"

    @classmethod
    def choices(obj):
        return tuple((item.value, item.name) for item in obj)


class OrderStatus(str, Enum):
    PLACED = "placed"
    PROCESSED = "processed"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    RETURN_PLACED = "return_placed"
    RETURN_PICKED = "return_picked"
    RETURN_PROCESSED = "return_processed"
    RETURN_SHIPPED = "return_shipped"
    RETURN_DELIVERED = "return_delivered"

    @classmethod
    def choices(obj):
        return tuple((item.value, item.name) for item in obj)


class Discount(Model):
    discount_code = CharField(max_length=16)
    type = CharField(max_length=32, choices=DiscountTypes.choices())
    mode = CharField(max_length=32, choices=PaymentModes.choices(), blank=True, null=True)
    value_type = CharField(max_length=32, choices=DiscountValueTypes.choices())
    value = FloatField(default=0)
    valid_from = DateTimeField(default=timezone.now)
    valid_to = DateTimeField(default=timezone.now)


class Product(Model):
    product_code = CharField(max_length=64)
    name = CharField(max_length=255)
    rating = PositiveSmallIntegerField(default=None, validators=[MinValueValidator(1), MaxValueValidator(5)])
    price = FloatField(default=0)
    discount = ForeignKey(Discount, on_delete=DO_NOTHING, blank=True, null=True)
    discounted_price = FloatField(default=0)
    description = TextField()
    # images
    # questions


# class Listing(Model):
#     product = ForeignKey(Product, on_delete=DO_NOTHING, related_name="product")
#     discount = ForeignKey(Discount, on_delete=DO_NOTHING, blank=True, null=True)
#     discounted_price = FloatField(default=0)
#     description = TextField()


class Review(Model):
    product = ForeignKey(Product, on_delete=DO_NOTHING, related_name="product")
    title = CharField(max_length=64)
    description = TextField()
    rating = PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    reviewer = ForeignKey(User, on_delete=DO_NOTHING, related_name="reviewer")
    verified = models.BooleanField(default=False)


class Order(Model):
    products = ManyToManyField(Product)
    buyer = ForeignKey(User, on_delete=DO_NOTHING, related_name="buyer")
    seller = ForeignKey(User, on_delete=DO_NOTHING, related_name="seller")
    value = FloatField(default=0)
    status = CharField(max_length=32, choices=OrderStatus.choices())
    created = DateTimeField(default=timezone.now)
    updated = DateTimeField(default=timezone.now)
    # type_for_buyer, eg: standard, expedited


class Payment(Model):
    order = ForeignKey(Order, on_delete=DO_NOTHING)
    status = CharField(max_length=32, choices=PaymentStatus.choices())
    mode = CharField(max_length=32, choices=PaymentModes.choices())
    gross_amount = FloatField(default=0)
    discount = ForeignKey(Discount, on_delete=DO_NOTHING, blank=True, null=True)
    net_amount = FloatField(default=0)


register(Discount)
register(Product)
register(Review)
register(Order)
register(Payment)
