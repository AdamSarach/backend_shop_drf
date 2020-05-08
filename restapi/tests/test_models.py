from rest_framework.test import APITestCase
from restapi.models import Supplier, Product, User, Order


class TestModelSupplier(APITestCase):

    def setUp(self):
        self.test_supplier = Supplier.objects.create(sup_name='Pipes Inc.',
                                                     sup_status='',
                                                     sup_email='pipesinc@pipesinc.com',
                                                     sup_phone_number=444555666,
                                                     sup_postal_code='00-220',
                                                     sup_city='Warsaw',
                                                     sup_address='Wiejska 12')

    def test_supplier_name(self):
        self.assertEquals(self.test_supplier.sup_name, 'Pipes Inc.')
        self.assertNotEquals(self.test_supplier.sup_name, 'NOT Pipes Inc.')


class TestModelProduct(APITestCase):

    def setUp(self):
        self.test_supplier = Supplier.objects.create(sup_name='Pipes Inc.',
                                                     sup_status='',
                                                     sup_email='pipesinc@pipesinc.com',
                                                     sup_phone_number=444555666,
                                                     sup_postal_code='00-220',
                                                     sup_city='Warsaw',
                                                     sup_address='Wiejska 12')
        self.test_product = Product.objects.create(pr_name='316 SS',
                                                   pr_sup=self.test_supplier,
                                                   pr_cat='PI',
                                                   pr_price=949.99)

    def test_product_name(self):
        self.assertEquals(self.test_product.pr_name, '316 SS')
        # self.assertNotEquals(self.test_supplier.sup_name, 'NOT 316 SS')
        # self.assertEquals(self.test_product.pr_sup.sup_id, self.test_supplier.sup_id)


class TestModelOrder(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='firstuser',
                                             password='testpass1')
        self.test_order = Order.objects.create(or_username=self.test_user)

    def test_order_username(self):
        self.assertEquals(self.test_user.username, 'firstuser')
        self.assertNotEquals(self.test_user.username, 'seconduser')
        self.assertIsNotNone(self.test_order.or_start_date)

