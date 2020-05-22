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

    def setUp(self):
        self.client = APIClient()

        self.data_valid = {
            "sup_name": "Pipe Valves",
            "sup_status": "",
            "sup_email": "pipevalves@pipevalves.com",
            "sup_phone_number": 444555666,
            "sup_postal_code": "00-220",
            "sup_city": "Warsaw",
            "sup_address": "Wiejska 12"

        }
        self.data_invalid = {
            "sup_name": "",
            "sup_status": "",
            "sup_email": "pipevalves@pipevalves.com",
            "sup_phone_number": 444555666,
            "sup_postal_code": "00-220",
            "sup_city": "Warsaw",
            "sup_address": "Wiejska 12"

        }
        self.group_employee = GroupFactory(name='employee')
        self.pwd = 'secret_pass'
        self.user_employee = UserFactory(password=self.pwd)
        self.user_employee.groups.add(self.group_employee)
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.url = reverse('supplier-list')

    def test_supplier_list_create(self):
        self.assertTrue(self.client.login(username=self.user_employee.username, password=self.pwd))
        response_valid = self.client.post(self.url, self.data_valid, format='json')
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        response_invalid = self.client.post(self.url, self.data_invalid, format='json')
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_supplier_list_retrieve(self):
        for _ in range(3):
            SupplierFactory()
        response = self.client.get(self.url)
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        self.assertEqual(Supplier.objects.count(), 3)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSupplierDetailView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_supplier = SupplierFactory()
        self.group_employee = GroupFactory(name='employee')
        self.pwd = 'secret_pass'
        self.user_employee = UserFactory(password=self.pwd)
        self.user_employee.groups.add(self.group_employee)
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.url = reverse('supplier-detail', kwargs={'pk': self.test_supplier.sup_id})

    def test_supplier_detail_retrieve(self):
        response = self.client.get(self.url)
        get_sup1 = Supplier.objects.get(pk=self.sup1.sup_id)
        serializer = SupplierSerializer(get_sup1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_detail_update(self):
        self.data = SupplierSerializer(self.test_supplier).data
        self.data.update({'sup_postal_code': '22-100'})
        response = self.client.put(reverse('supplier-detail', args=[self.test_supplier.sup_id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_detail_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestProductListView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_supplier = SupplierFactory()
        self.data_valid = {
            "pr_name": "304 SS",
            "pr_cat": "PI",
            "pr_price": 200.55,
            "pr_sup": self.test_supplier.sup_id,

        }
        self.data_invalid = {
            "pr_name": "304 SS",
            "pr_cat": "PA",
            "pr_price": 200.55,
            "pr_sup": self.test_supplier.sup_id,
        }
        self.group_employee = GroupFactory(name='employee')
        self.pwd = 'secret_pass'
        self.user_employee = UserFactory(password=self.pwd)
        self.user_employee.groups.add(self.group_employee)
        self.url = reverse('product-list')

    def test_product_list_create(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        response_valid = self.client.post(self.url, self.data_valid, format='json')
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        response_invalid = self.client.post(self.url, self.data_invalid, format='json')
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_list_retrieve(self):
        for _ in range(3):
            ProductFactory(pr_sup=self.test_supplier)
        response = self.client.get(self.url)
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProductDetailView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_supplier = SupplierFactory()
        self.test_product = ProductFactory(pr_sup=self.test_supplier)
        self.group_employee = GroupFactory(name='employee')
        self.pwd = 'secret_pass'
        self.user_employee = UserFactory(password=self.pwd)
        self.user_employee.groups.add(self.group_employee)
        self.url = reverse('product-detail', kwargs={'pk': self.test_product.pr_id})

    def test_product_detail_retrieve(self):
        response = self.client.get(self.url)
        get_pr1 = Product.objects.get(pk=self.test_product.pr_id)
        serializer = ProductSerializer(get_pr1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_update(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.data = ProductSerializer(self.test_product).data
        self.data.update({'pr_price': 1299.99})
        response = self.client.put(reverse('product-detail', args=[self.test_product.pr_id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_delete(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderListView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.group_employee = GroupFactory(name='employee')
        self.group_customer = GroupFactory(name='customer')
        self.pwd = 'secret_pass'
        self.user_employee = UserFactory(password=self.pwd)
        self.user_employee.groups.add(self.group_employee)
        self.user_customer1 = UserFactory(password=self.pwd)
        self.user_customer1.groups.add(self.group_customer)
        self.user_customer2 = UserFactory(password=self.pwd)
        self.user_customer2.groups.add(self.group_customer)

        # Sample orders to check[GET] for list
        self.test_order1 = OrderFactory(or_username=self.user_customer1)
        self.test_order2 = OrderFactory(or_username=self.user_customer1)
        self.test_order3 = OrderFactory(or_username=self.user_customer2)
        self.test_order4 = OrderFactory(or_username=self.user_employee)

        self.url = reverse('order-list')

    def test_order_list_retrieve_customer(self):
        self.client.login(username=self.user_customer1.username, password=self.pwd)
        self.assertTrue(self.client.login(username=self.user_customer1.username, password=self.pwd))
        response = self.client.get(self.url)
        order = Order.objects.filter(or_username=self.user_customer1)
        serializer = OrderSerializer(order, many=True)
        self.assertEqual(order.count(), 2)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_retrieve_employee(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.assertTrue(self.client.login(username=self.user_employee.username, password=self.pwd))
        response = self.client.get(self.url)
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        self.assertEqual(order.count(), 4)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_create_customer(self):
        self.client.login(username=self.user_customer1.username, password=self.pwd)
        self.data = {}
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_list_create_employee(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.data_valid = {'or_username': self.user_customer1.id}
        self.data_invalid = {}
        response_valid = self.client.post(self.url, self.data_valid, format='json')
        response_invalid = self.client.post(self.url, self.data_invalid, format='json')
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list_create_retrieve_unauthenticated(self):
        self.data1 = {'or_username': self.user_customer1.id}
        self.data2 = {}
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, status.HTTP_403_FORBIDDEN)
        response_post1 = self.client.post(self.url, self.data1, format='json')
        self.assertEqual(response_post1.status_code, status.HTTP_403_FORBIDDEN)
        response_post2 = self.client.post(self.url, self.data1, format='json')
        self.assertEqual(response_post2.status_code, status.HTTP_403_FORBIDDEN)


class TestOrderDetailView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.group_employee = GroupFactory(name='employee')
        self.group_customer = GroupFactory(name='customer')
        self.pwd = 'secret_pass'
        self.user_employee = UserFactory(password=self.pwd)
        self.user_employee.groups.add(self.group_employee)
        self.user_customer1 = UserFactory(password=self.pwd)
        self.user_customer1.groups.add(self.group_customer)
        self.user_customer2 = UserFactory(password=self.pwd)
        self.user_customer2.groups.add(self.group_customer)
        self.test_order1 = OrderFactory(or_username=self.user_customer1)
        self.test_order2 = OrderFactory(or_username=self.user_customer1, or_is_finished=True)
        self.test_order3 = OrderFactory(or_username=self.user_customer2)
        self.test_order4 = OrderFactory(or_username=self.user_employee)
        self.test_supplier = SupplierFactory()
        self.test_product1 = ProductFactory(pr_sup=self.test_supplier)
        self.test_product2 = ProductFactory(pr_sup=self.test_supplier)
        self.test_product3 = ProductFactory(pr_sup=self.test_supplier)
        self.url = reverse('order-detail', kwargs={'pk': self.test_order1.or_id})
        self.url_another_customer = reverse('order-detail', kwargs={'pk': self.test_order3.or_id})

    def test_order_detail_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_delete = self.client.delete(self.url)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_detail_retrieve_employee(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_retrieve_customer(self):
        self.client.login(username=self.user_customer1.username, password=self.pwd)
        response = self.client.get(self.url)
        get_or1 = Order.objects.get(pk=self.test_order1.or_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_another = self.client.get(self.url_another_customer)
        self.assertEqual(response_another.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_update_employee(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.data = OrderSerializer(self.test_order1).data
        self.data.update({'or_username': self.user_customer2.id, 'or_is_sent': True})
        response = self.client.put(reverse('order-detail', args=[self.test_order1.or_id]), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_update_customer_valid(self):
        self.client.login(username=self.user_customer1.username, password=self.pwd)
        response_valid1 = self.client.put(reverse('order-detail', args=[self.test_order1.or_id]), format='json')
        self.assertEqual(response_valid1.status_code, status.HTTP_200_OK)

    def test_order_detail_update_customer_invalid(self):
        self.client.login(username=self.user_customer1.username, password=self.pwd)
        # Other customer's order
        response_invalid1 = self.client.put(reverse('order-detail', args=[self.test_order3.or_id]), format='json')
        self.assertEqual(response_invalid1.status_code, status.HTTP_400_BAD_REQUEST)
        # Order marked as finished
        response_invalid2 = self.client.put(reverse('order-detail', args=[self.test_order2.or_id]), format='json')
        self.assertEqual(response_invalid2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_delete_customer(self):
        self.client.login(username=self.user_customer1.username, password=self.pwd)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(self.url_another_customer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_delete_employee(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderItemsView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.group_employee = GroupFactory(name='employee')
        self.group_customer = GroupFactory(name='customer')
        self.pwd = 'secret_pass'
        self.user_employee = UserFactory(password=self.pwd)
        self.user_employee.groups.add(self.group_employee)
        self.user_customer1 = UserFactory(password=self.pwd)
        self.user_customer1.groups.add(self.group_customer)
        self.user_customer2 = UserFactory(password=self.pwd)
        self.user_customer2.groups.add(self.group_customer)
        self.test_order1 = OrderFactory(or_username=self.user_customer1)
        self.test_order2 = OrderFactory(or_username=self.user_customer1, or_is_finished=True)
        self.test_order3 = OrderFactory(or_username=self.user_customer2)
        self.test_order4 = OrderFactory(or_username=self.user_employee)
        self.test_supplier = SupplierFactory()
        self.test_product1 = ProductFactory(pr_sup=self.test_supplier)
        self.test_product2 = ProductFactory(pr_sup=self.test_supplier)
        self.url = reverse('order-item', kwargs={'pk': self.test_order1.or_id})
        self.url_another_customer = reverse('order-item', kwargs={'pk': self.test_order3.or_id})
        self.url_finished = reverse('order-item', kwargs={'pk': self.test_order2.or_id})

    def test_order_item_create_employee(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.data = {"pr_id": self.test_product2.pr_id, "amount": 25}
        response_valid = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)

    def test_order_item_create_customer(self):
        self.client.login(username=self.user_customer1.username, password=self.pwd)
        self.data = {"pr_id": self.test_product2.pr_id, "amount": 25}
        response_valid = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        response_invalid = self.client.post(self.url_another_customer, self.data, format='json')
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_item_check_uniqueness(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.pio1 = ProductsInOrdersFactory(or_id=self.test_order1,
                                            pr_id=self.test_product1)
        self.data = {"pr_id": self.test_product1.pr_id, "amount": self.pio1.amount}
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_item_check_finished_order(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.data = {"pr_id": self.test_product2.pr_id, "amount": 25}
        response_valid = self.client.post(self.url_finished, self.data, format='json')
        self.assertEqual(response_valid.status_code, status.HTTP_400_BAD_REQUEST)


class TestOrderItemDetailView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.group_employee = GroupFactory(name='employee')
        self.group_customer = GroupFactory(name='customer')
        self.pwd = 'secret_pass'
        self.user_employee = UserFactory(password=self.pwd)
        self.user_employee.groups.add(self.group_employee)
        self.user_customer1 = UserFactory(password=self.pwd)
        self.user_customer1.groups.add(self.group_customer)
        self.user_customer2 = UserFactory(password=self.pwd)
        self.user_customer2.groups.add(self.group_customer)
        self.test_order1 = OrderFactory(or_username=self.user_customer1)
        self.test_order2 = OrderFactory(or_username=self.user_customer1, or_is_finished=True)
        self.test_order3 = OrderFactory(or_username=self.user_customer2)
        self.test_order4 = OrderFactory(or_username=self.user_employee)
        self.test_supplier = SupplierFactory()
        self.test_product1 = ProductFactory(pr_sup=self.test_supplier)
        self.test_product2 = ProductFactory(pr_sup=self.test_supplier)
        self.pio1 = ProductsInOrdersFactory(or_id=self.test_order1,
                                            pr_id=self.test_product1)
        self.pio2 = ProductsInOrdersFactory(or_id=self.test_order1,
                                            pr_id=self.test_product2)
        self.pio3 = ProductsInOrdersFactory(or_id=self.test_order2,
                                            pr_id=self.test_product2)
        self.url = reverse('order-item-detail', kwargs={'pk': self.test_order1.or_id, 'item': self.pio1.id})

    def test_order_item_detail_update_employee(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        self.data = ProductsInOrdersSerializer(self.pio1).data
        self.data.update({'amount': 5})
        response = self.client.put(
            reverse('order-item-detail', kwargs={'pk': self.test_order1.or_id, 'item': self.pio1.id}),
            self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_item_detail_delete_employee(self):
        self.client.login(username=self.user_employee.username, password=self.pwd)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
