from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Sum, F, ExpressionWrapper, DecimalField


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Supplier(models.Model):
    """Keep suppliers' personal data."""
    sup_id = models.AutoField(primary_key=True)
    sup_name = models.CharField(max_length=50, unique=True)
    sup_status = models.CharField(max_length=30, blank=True)
    sup_email = models.EmailField()
    sup_phone_number = models.IntegerField()
    sup_postal_code = models.CharField(max_length=10)
    sup_city = models.CharField(max_length=50)
    sup_address = models.CharField(max_length=70)

    def __str__(self):
        return self.sup_name

    @property
    def full_address(self):
        """The full way of addressing a supplier"""
        return '{}, {}, {} {}'.format(self.sup_name, self.sup_address, self.sup_postal_code, self.sup_city)


class Product(models.Model):
    PIPES = 'PI'
    FITTINGS = 'FI'
    VALVES = 'VA'
    WELD_AND_THREAD = 'WT'
    CATEGORY_CHOICES = [(PIPES, 'Pipes'),
                        (FITTINGS, 'Fittings'),
                        (VALVES, 'Valves'),
                        (WELD_AND_THREAD, 'Welds and threads')]

    pr_id = models.AutoField(primary_key=True)
    pr_name = models.CharField(max_length=50)
    pr_cat = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    pr_price = models.DecimalField(max_digits=8, decimal_places=2)
    pr_sup = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    def __str__(self):
        return self.pr_name


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Order(models.Model):
    or_id = models.AutoField(primary_key=True)
    or_start_date = models.DateTimeField(auto_now_add=True)
    or_is_finished = models.BooleanField(default=False)
    or_finish_date = models.DateTimeField(null=True)
    or_is_sent = models.BooleanField(default=False)
    or_sent_date = models.DateTimeField(null=True)
    or_username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return 'Order No. {}, started {}'.format(self.or_id, self.or_start_date)

    @property
    def total_price(self):
        order_price = self.items_in_order.all().aggregate(
            price=ExpressionWrapper(Sum(F('amount') * F('pr_id__pr_price')), output_field=DecimalField()))
        return order_price


class ProductsInOrders(models.Model):
    or_id = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items_in_order', db_column='or_id')
    pr_id = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='chosen_products', db_column='pr_id')
    amount = models.IntegerField()

    def __str__(self):
        return 'Order No. {}, Product: {}, Amount: {}'.format(self.or_id.or_id, self.pr_id.pr_name, self.amount)
