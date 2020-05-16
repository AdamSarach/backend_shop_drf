import factory
from restapi.models import Supplier


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    sup_id = factory.Sequence(lambda n: n)
    sup_name = factory.Sequence(lambda n: 'Supplier%d' % n)
    sup_status = 'Undefined'
    sup_email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.sup_name)
    sup_phone_number = factory.Faker('msisdn')
    sup_postal_code = factory.Faker('postcode')
    sup_city = factory.Faker('city')
    sup_address = factory.Faker('street_address')
