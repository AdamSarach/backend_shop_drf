from rest_framework.test import APITestCase
from restapi.models import Supplier, Product, Order, ProductsInOrders
from restapi.factories import SupplierFactory, ProductFactory, UserFactory, OrderFactory, ProductsInOrdersFactory, \
    GroupFactory


class TestModelSupplier(APITestCase):

    def setUp(self):
        self.test_supplier = SupplierFactory()

    def test_supplier_name(self):
        self.assertIsInstance(self.test_supplier, Supplier)


class TestModelProduct(APITestCase):

    def setUp(self):
        self.test_supplier = SupplierFactory()
        self.test_product = ProductFactory(pr_sup=self.test_supplier)

    def test_product_name(self):
        self.assertIsInstance(self.test_product, Product)
        self.assertEquals(self.test_product.pr_sup.sup_id, self.test_supplier.sup_id)


class TestModelOrder(APITestCase):

    def setUp(self):
        self.test_user = UserFactory()
        self.test_order = OrderFactory(or_username=self.test_user)

    def test_order_username(self):
        self.assertIsInstance(self.test_order, Order)
        self.assertIsNotNone(self.test_order.or_start_date)


class TestModelProductsInOrder(APITestCase):

    def setUp(self):
        self.test_user = UserFactory()
        self.test_order = OrderFactory(or_username=self.test_user)
        self.test_supplier = SupplierFactory()
        self.test_product = ProductFactory(pr_sup=self.test_supplier)

    def test_products_in_order_isinstance(self):
        self.test_item = ProductsInOrdersFactory(or_id=self.test_order, pr_id=self.test_product)
        self.assertIsInstance(self.test_item, ProductsInOrders)


class TestModelUser(APITestCase):

    def setUp(self):
        self.group_employee = GroupFactory(name='employee')
        self.user_employee = UserFactory()
        self.user_employee.groups.add(self.group_employee)

    def test_is_user_in_group(self):
        self.assertEqual(self.user_employee.groups.filter(name='employee').exists(), True)
        self.assertEqual(self.user_employee.groups.filter(name='customer').exists(), False)
