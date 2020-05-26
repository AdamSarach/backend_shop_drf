from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from restapi.models import Supplier, Product, Order, User, ProductsInOrders
from restapi.serializers import SupplierSerializer, ProductSerializer, OrderSerializer, ProductsInOrdersSerializer
from django.contrib.auth.models import Group
from restapi.factories import GroupFactory, UserFactory, SupplierFactory, ProductFactory, OrderFactory, \
    ProductsInOrdersFactory


class TestSupplierListView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse('supplier-list')
        cls.url_token = reverse('token')
        cls.data_valid = {
            "sup_name": "Pipe Valves",
            "sup_status": "",
            "sup_email": "pipevalves@pipevalves.com",
            "sup_phone_number": 444555666,
            "sup_postal_code": "00-220",
            "sup_city": "Warsaw",
            "sup_address": "Wiejska 12"
        }
        cls.data_invalid = {
            "sup_name": "",
            "sup_status": "",
            "sup_email": "pipevalves@pipevalves.com",
            "sup_phone_number": 444555666,
            "sup_postal_code": "00-220",
            "sup_city": "Warsaw",
            "sup_address": "Wiejska 12"
        }
        cls.group_employee = GroupFactory(name='employee')
        cls.pwd = 'secret_pass'
        cls.user_employee = UserFactory(password=cls.pwd)
        cls.user_employee.groups.add(cls.group_employee)

    def setUp(self):
        self.user_token_emp = self.client.post(
            self.url_token,
            data={'username': self.user_employee.username, 'password': self.pwd}).data['access']
        self.user_header = 'Bearer ' + self.user_token_emp

    def test_supplier_list_create(self):
        response_valid = self.client.post(self.url, self.data_valid, format='json', HTTP_AUTHORIZATION=self.user_header)
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        response_invalid = self.client.post(self.url, self.data_invalid, format='json',
                                            HTTP_AUTHORIZATION=self.user_header)
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_supplier_list_retrieve(self):
        for _ in range(3):
            SupplierFactory()
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.user_header)
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        self.assertEqual(Supplier.objects.count(), 3)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSupplierDetailView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_supplier = SupplierFactory()
        cls.url = reverse('supplier-detail', kwargs={'pk': cls.test_supplier.sup_id})
        cls.url_token = reverse('token')
        cls.group_employee = GroupFactory(name='employee')
        cls.pwd = 'secret_pass'
        cls.user_employee = UserFactory(password=cls.pwd)
        cls.user_employee.groups.add(cls.group_employee)

    def setUp(self):
        self.user_token_employee = self.client.post(
            self.url_token,
            data={'username': self.user_employee.username, 'password': self.pwd}).data['access']
        self.user_header_employee = 'Bearer ' + self.user_token_employee

    def test_supplier_detail_retrieve(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.user_header_employee)
        get_sup1 = Supplier.objects.get(pk=self.test_supplier.sup_id)
        serializer = SupplierSerializer(get_sup1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_detail_update(self):
        self.data = SupplierSerializer(self.test_supplier).data
        self.data.update({'sup_postal_code': '22-100'})
        response = self.client.put(reverse('supplier-detail', args=[self.test_supplier.sup_id]), self.data,
                                   HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_detail_delete(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestProductListView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse('product-list')
        cls.url_token = reverse('token')
        cls.test_supplier = SupplierFactory()
        cls.data_valid = {
            "pr_name": "304 SS",
            "pr_cat": "PI",
            "pr_price": 200.55,
            "pr_sup": cls.test_supplier.sup_id,
        }
        cls.data_invalid = {
            "pr_name": "304 SS",
            "pr_cat": "PA",
            "pr_price": 200.55,
            "pr_sup": cls.test_supplier.sup_id,
        }
        cls.group_employee = GroupFactory(name='employee')
        cls.pwd = 'secret_pass'
        cls.user_employee = UserFactory(password=cls.pwd)
        cls.user_employee.groups.add(cls.group_employee)

    def setUp(self):
        self.user_token_employee = self.client.post(
            self.url_token,
            data={'username': self.user_employee.username, 'password': self.pwd}).data['access']
        self.user_header_employee = 'Bearer ' + self.user_token_employee

    def test_product_list_create(self):
        response_valid = self.client.post(self.url, self.data_valid, format='json',
                                          HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        response_invalid = self.client.post(self.url, self.data_invalid, format='json',
                                            HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_list_retrieve(self):
        for _ in range(3):
            ProductFactory(pr_sup=self.test_supplier)
        response = self.client.get(self.url)
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProductDetailView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_supplier = SupplierFactory()
        cls.test_product = ProductFactory(pr_sup=cls.test_supplier)
        cls.group_employee = GroupFactory(name='employee')
        cls.pwd = 'secret_pass'
        cls.user_employee = UserFactory(password=cls.pwd)
        cls.user_employee.groups.add(cls.group_employee)
        cls.url = reverse('product-detail', kwargs={'pk': cls.test_product.pr_id})
        cls.url_token = reverse('token')

    def setUp(self):
        self.user_token_employee = self.client.post(
            self.url_token,
            data={'username': self.user_employee.username, 'password': self.pwd}).data['access']
        self.user_header_employee = 'Bearer ' + self.user_token_employee

    def test_product_detail_retrieve(self):
        response = self.client.get(self.url)
        get_pr1 = Product.objects.get(pk=self.test_product.pr_id)
        serializer = ProductSerializer(get_pr1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_update(self):
        self.data = ProductSerializer(self.test_product).data
        self.data.update({'pr_price': 1299.99})
        response = self.client.put(reverse('product-detail', args=[self.test_product.pr_id]), self.data,
                                   HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_delete(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderListView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.group_employee = GroupFactory(name='employee')
        cls.group_customer = GroupFactory(name='customer')
        cls.pwd = 'secret_pass'
        cls.user_employee = UserFactory(password=cls.pwd)
        cls.user_employee.groups.add(cls.group_employee)
        cls.user_customer1 = UserFactory(password=cls.pwd)
        cls.user_customer1.groups.add(cls.group_customer)
        cls.user_customer2 = UserFactory(password=cls.pwd)
        cls.user_customer2.groups.add(cls.group_customer)

        # Sample orders to check[GET] for list
        cls.test_order1 = OrderFactory(or_username=cls.user_customer1)
        cls.test_order2 = OrderFactory(or_username=cls.user_customer1)
        cls.test_order3 = OrderFactory(or_username=cls.user_customer2)
        cls.test_order4 = OrderFactory(or_username=cls.user_employee)

        cls.url = reverse('order-list')
        cls.url_token = reverse('token')

    def setUp(self):
        self.user_token_employee = self.client.post(
            self.url_token,
            data={'username': self.user_employee.username, 'password': self.pwd}).data['access']
        self.user_header_employee = 'Bearer ' + self.user_token_employee

        self.user_token_customer1 = self.client.post(
            self.url_token,
            data={'username': self.user_customer1.username, 'password': self.pwd}).data['access']
        self.user_header_customer1 = 'Bearer ' + self.user_token_customer1

    def test_order_list_retrieve_customer(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.user_header_customer1)
        order = Order.objects.filter(or_username=self.user_customer1)
        serializer = OrderSerializer(order, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_retrieve_employee(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.user_header_employee)
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_create_customer(self):
        self.data = {}
        response = self.client.post(self.url, self.data, format='json', HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_list_create_employee(self):
        self.data_valid = {'or_username': self.user_customer1.id}
        self.data_invalid = {}
        response_valid = self.client.post(self.url, self.data_valid, format='json',
                                          HTTP_AUTHORIZATION=self.user_header_employee)
        response_invalid = self.client.post(self.url, self.data_invalid, format='json',
                                            HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list_create_retrieve_unauthenticated(self):
        self.data1 = {'or_username': self.user_customer1.id}
        self.data2 = {}
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, status.HTTP_401_UNAUTHORIZED)
        response_post1 = self.client.post(self.url, self.data1, format='json')
        self.assertEqual(response_post1.status_code, status.HTTP_401_UNAUTHORIZED)
        response_post2 = self.client.post(self.url, self.data1, format='json')
        self.assertEqual(response_post2.status_code, status.HTTP_401_UNAUTHORIZED)


class TestOrderDetailView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.group_employee = GroupFactory(name='employee')
        cls.group_customer = GroupFactory(name='customer')
        cls.pwd = 'secret_pass'
        cls.user_employee = UserFactory(password=cls.pwd)
        cls.user_employee.groups.add(cls.group_employee)
        cls.user_customer1 = UserFactory(password=cls.pwd)
        cls.user_customer1.groups.add(cls.group_customer)
        cls.user_customer2 = UserFactory(password=cls.pwd)
        cls.user_customer2.groups.add(cls.group_customer)
        cls.test_order2 = OrderFactory(or_username=cls.user_customer1, or_is_finished=True)
        cls.test_order3 = OrderFactory(or_username=cls.user_customer2)
        cls.test_order4 = OrderFactory(or_username=cls.user_employee)
        cls.test_supplier = SupplierFactory()
        cls.test_product1 = ProductFactory(pr_sup=cls.test_supplier)
        cls.test_product2 = ProductFactory(pr_sup=cls.test_supplier)
        cls.test_product3 = ProductFactory(pr_sup=cls.test_supplier)
        cls.url_another_customer = reverse('order-detail', kwargs={'pk': cls.test_order3.or_id})
        cls.url_token = reverse('token')

    def setUp(self):
        self.test_order1 = OrderFactory(or_username=self.user_customer1)
        self.url = reverse('order-detail', kwargs={'pk': self.test_order1.or_id})

        self.user_token_employee = self.client.post(
            self.url_token,
            data={'username': self.user_employee.username, 'password': self.pwd}).data['access']
        self.user_header_employee = 'Bearer ' + self.user_token_employee

        self.user_token_customer1 = self.client.post(
            self.url_token,
            data={'username': self.user_customer1.username, 'password': self.pwd}).data['access']
        self.user_header_customer1 = 'Bearer ' + self.user_token_customer1

    def test_order_detail_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_delete = self.client.delete(self.url)
        self.assertEqual(response_delete.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_detail_retrieve_employee(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_retrieve_customer(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_another = self.client.get(self.url_another_customer, HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response_another.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_update_employee(self):
        self.data = OrderSerializer(self.test_order1).data
        self.data.update({'or_username': self.user_customer2.id, 'or_is_sent': True})
        response = self.client.put(reverse('order-detail', args=[self.test_order1.or_id]), self.data, format='json',
                                   HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_update_customer_valid(self):
        response_valid1 = self.client.put(reverse('order-detail', args=[self.test_order1.or_id]), format='json',
                                          HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response_valid1.status_code, status.HTTP_200_OK)

    def test_order_detail_update_customer_invalid(self):
        # Other customer's order
        response_invalid1 = self.client.put(reverse('order-detail', args=[self.test_order3.or_id]), format='json',
                                            HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response_invalid1.status_code, status.HTTP_400_BAD_REQUEST)
        # Order marked as finished
        response_invalid2 = self.client.put(reverse('order-detail', args=[self.test_order2.or_id]), format='json',
                                            HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response_invalid2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_delete_customer(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(self.url_another_customer, HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_delete_employee(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderItemsView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.group_employee = GroupFactory(name='employee')
        cls.group_customer = GroupFactory(name='customer')
        cls.pwd = 'secret_pass'
        cls.user_employee = UserFactory(password=cls.pwd)
        cls.user_employee.groups.add(cls.group_employee)
        cls.user_customer1 = UserFactory(password=cls.pwd)
        cls.user_customer1.groups.add(cls.group_customer)
        cls.user_customer2 = UserFactory(password=cls.pwd)
        cls.user_customer2.groups.add(cls.group_customer)
        cls.test_order1 = OrderFactory(or_username=cls.user_customer1)
        cls.test_order2 = OrderFactory(or_username=cls.user_customer1, or_is_finished=True)
        cls.test_order3 = OrderFactory(or_username=cls.user_customer2)
        cls.test_order4 = OrderFactory(or_username=cls.user_employee)
        cls.test_supplier = SupplierFactory()
        cls.test_product1 = ProductFactory(pr_sup=cls.test_supplier)
        cls.test_product2 = ProductFactory(pr_sup=cls.test_supplier)
        cls.url = reverse('order-item', kwargs={'pk': cls.test_order1.or_id})
        cls.url_another_customer = reverse('order-item', kwargs={'pk': cls.test_order3.or_id})
        cls.url_finished = reverse('order-item', kwargs={'pk': cls.test_order2.or_id})
        cls.url_token = reverse('token')

    def setUp(self):
        self.user_token_employee = self.client.post(
            self.url_token,
            data={'username': self.user_employee.username, 'password': self.pwd}).data['access']
        self.user_header_employee = 'Bearer ' + self.user_token_employee

        self.user_token_customer1 = self.client.post(
            self.url_token,
            data={'username': self.user_customer1.username, 'password': self.pwd}).data['access']
        self.user_header_customer1 = 'Bearer ' + self.user_token_customer1

    def test_order_item_create_employee(self):
        self.data = {"pr_id": self.test_product2.pr_id, "amount": 25}
        response_valid = self.client.post(self.url, self.data, format='json',
                                          HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)

    def test_order_item_create_customer(self):
        self.data = {"pr_id": self.test_product2.pr_id, "amount": 25}
        response_valid = self.client.post(self.url, self.data, format='json',
                                          HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        response_invalid = self.client.post(self.url_another_customer, self.data, format='json',
                                            HTTP_AUTHORIZATION=self.user_header_customer1)
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_item_check_uniqueness(self):
        self.pio1 = ProductsInOrdersFactory(or_id=self.test_order1,
                                            pr_id=self.test_product1)
        self.data = {"pr_id": self.test_product1.pr_id, "amount": self.pio1.amount}
        response = self.client.post(self.url, self.data, format='json', HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_item_check_finished_order(self):
        self.data = {"pr_id": self.test_product2.pr_id, "amount": 25}
        response_valid = self.client.post(self.url_finished, self.data, format='json',
                                          HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response_valid.status_code, status.HTTP_400_BAD_REQUEST)


class TestOrderItemDetailView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.group_employee = GroupFactory(name='employee')
        cls.group_customer = GroupFactory(name='customer')
        cls.pwd = 'secret_pass'
        cls.user_employee = UserFactory(password=cls.pwd)
        cls.user_employee.groups.add(cls.group_employee)
        cls.user_customer1 = UserFactory(password=cls.pwd)
        cls.user_customer1.groups.add(cls.group_customer)
        cls.user_customer2 = UserFactory(password=cls.pwd)
        cls.user_customer2.groups.add(cls.group_customer)
        cls.test_order1 = OrderFactory(or_username=cls.user_customer1)
        cls.test_order2 = OrderFactory(or_username=cls.user_customer1, or_is_finished=True)
        cls.test_order3 = OrderFactory(or_username=cls.user_customer2)
        cls.test_order4 = OrderFactory(or_username=cls.user_employee)
        cls.test_supplier = SupplierFactory()
        cls.test_product1 = ProductFactory(pr_sup=cls.test_supplier)
        cls.test_product2 = ProductFactory(pr_sup=cls.test_supplier)
        cls.pio1 = ProductsInOrdersFactory(or_id=cls.test_order1,
                                           pr_id=cls.test_product1)
        cls.pio2 = ProductsInOrdersFactory(or_id=cls.test_order1,
                                           pr_id=cls.test_product2)
        cls.pio3 = ProductsInOrdersFactory(or_id=cls.test_order2,
                                           pr_id=cls.test_product2)
        cls.url = reverse('order-item-detail', kwargs={'pk': cls.test_order1.or_id, 'item': cls.pio1.id})
        cls.url_token = reverse('token')

    def setUp(self):
        self.user_token_employee = self.client.post(
            self.url_token,
            data={'username': self.user_employee.username, 'password': self.pwd}).data['access']
        self.user_header_employee = 'Bearer ' + self.user_token_employee

        self.user_token_customer1 = self.client.post(
            self.url_token,
            data={'username': self.user_customer1.username, 'password': self.pwd}).data['access']
        self.user_header_customer1 = 'Bearer ' + self.user_token_customer1

    def test_order_item_detail_update_employee(self):
        self.data = ProductsInOrdersSerializer(self.pio1).data
        self.data.update({'amount': 5})
        response = self.client.put(
            reverse('order-item-detail', kwargs={'pk': self.test_order1.or_id, 'item': self.pio1.id}),
            self.data, format='json', HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_item_detail_delete_employee(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.user_header_employee)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
