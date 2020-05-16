import factory
from restapi.models import Supplier, Product, Order, User, ProductsInOrders
from django.contrib.auth.models import Group
import factory.fuzzy
import datetime


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'User%d' % (n + 1))
    password = 'abc123'


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    sup_id = factory.Sequence(lambda n: (n + 1))
    sup_name = factory.Sequence(lambda n: 'Supplier%d' % (n + 1))
    sup_status = 'Undefined'
    sup_email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.sup_name)
    sup_phone_number = factory.Faker('msisdn')
    sup_postal_code = factory.Faker('postcode')
    sup_city = factory.Faker('city')
    sup_address = factory.Faker('street_address')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    pr_id = factory.Sequence(lambda n: n + 1)
    pr_name = factory.Sequence(lambda n: 'Product%d' % n)
    pr_cat = 'PI'
    pr_price = factory.fuzzy.FuzzyDecimal(1.00, 999999.99, 2)
    pr_sup = factory.SubFactory(SupplierFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    or_id = factory.Sequence(lambda n: n + 1)
    or_start_date = factory.LazyFunction(datetime.now)
    or_username = factory.SubFactory(UserFactory)


class ProductsInOrdersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductsInOrders

    or_id = factory.SubFactory(UserFactory)
    pr_id = factory.SubFactory(UserFactory)
    amount = factory.fuzzy.FuzzyInteger(1, 1000)
