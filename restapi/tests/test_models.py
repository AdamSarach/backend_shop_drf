from django.test import TestCase
from restapi.models import Supplier


class TestModelSupplier(TestCase):

    def setUp(self):
        self.test_supplier = Supplier.objects.create(sup_id=1001,
                                                     sup_name='Pipes Inc.',
                                                     sup_status='',
                                                     sup_email='pipesinc@pipesinc.com',
                                                     sup_phone_number=444555666,
                                                     sup_postal_code='00-220',
                                                     sup_city='Warsaw',
                                                     sup_address='Wiejska 12')

    def test_supplier_name(self):
        self.assertEquals(self.test_supplier.sup_name, 'Pipes Inc.')
        self.assertNotEquals(self.test_supplier.sup_name, 'NOT Pipes Inc.')


