from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from restapi.models import Supplier, Product, Order, User, ProductsInOrders
from restapi.serializers import SupplierSerializer, ProductSerializer, OrderSerializer
from django.contrib.auth.models import Group


class TestSupplierListView(APITestCase):

    def setUp(self):
        self.url = reverse('supplier-list')
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
        self.newsupplier = Supplier.objects.create(sup_name="Pipes Weld",
                                                   sup_status='',
                                                   sup_email='pipeweld@pipeweld.com',
                                                   sup_phone_number=222555666,
                                                   sup_postal_code='00-220',
                                                   sup_city='Warsaw',
                                                   sup_address='Wiejska 18'
                                                   )
        self.user_employee = User.objects.create_user(username='empnewbie',
                                                      password='testpass1')
        self.group_employee = Group.objects.create(name='employee')
        self.user_employee.save()
        self.user_employee.groups.add(self.group_employee)
        self.client.login(username='empnewbie', password='testpass1')

    def test_supplier_list_create(self):
        response_valid = self.client.post(self.url, self.data_valid, format='json')
        response_invalid = self.client.post(self.url, self.data_invalid, format='json')
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 2)
        self.assertEqual(Supplier.objects.get(sup_email="pipevalves@pipevalves.com").sup_name, 'Pipe Valves')

    def test_supplier_list_retrieve(self):
        response = self.client.get(self.url)
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSupplierDetailView(APITestCase):

    def setUp(self):
        self.sup1 = Supplier.objects.create(sup_name="Valves inc",
                                            sup_status='',
                                            sup_email='valves@valves.com',
                                            sup_phone_number=88855666,
                                            sup_postal_code='00-220',
                                            sup_city='Warsaw',
                                            sup_address='Wiejska 50'
                                            )
        self.url = reverse('supplier-detail', kwargs={'pk': self.sup1.sup_id})
        self.user_employee = User.objects.create_user(username='empnewbie',
                                                      password='testpass1')
        self.group_employee = Group.objects.create(name='employee')
        self.user_employee.save()
        self.user_employee.groups.add(self.group_employee)
        self.client.login(username='empnewbie', password='testpass1')

    def test_supplier_detail_retrieve(self):
        response = self.client.get(self.url)
        get_sup1 = Supplier.objects.get(pk=self.sup1.sup_id)
        serializer = SupplierSerializer(get_sup1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_detail_update(self):
        self.data = SupplierSerializer(self.sup1).data
        self.data.update({'sup_postal_code': '22-100'})
        response = self.client.put(reverse('supplier-detail', args=[self.sup1.sup_id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_detail_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestProductListView(APITestCase):

    def setUp(self):
        self.url = reverse('product-list')
        self.test_supplier = Supplier.objects.create(sup_name='Pipes World',
                                                     sup_status='',
                                                     sup_email='pipesinc@pipesinc.com',
                                                     sup_phone_number=444555666,
                                                     sup_postal_code='00-220',
                                                     sup_city='Warsaw',
                                                     sup_address='Wiejska 12')
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

        self.newproduct = Product.objects.create(pr_name='316 SS',
                                                 pr_cat='PI',
                                                 pr_price=1499.99,
                                                 pr_sup=self.test_supplier,
                                                 )
        self.user_employee = User.objects.create_user(username='empnewbie',
                                                      password='testpass1')
        self.group_employee = Group.objects.create(name='employee')
        self.user_employee.save()
        self.user_employee.groups.add(self.group_employee)

    def test_product_list_create(self):
        self.client.login(username='empnewbie', password='testpass1')
        response_valid = self.client.post(self.url, self.data_valid, format='json')
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)
        response_invalid = self.client.post(self.url, self.data_invalid, format='json')
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_list_retrieve(self):
        response = self.client.get(self.url)
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProductDetailView(APITestCase):

    def setUp(self):
        self.test_supplier = Supplier.objects.create(sup_name='Pipes World',
                                                     sup_status='',
                                                     sup_email='pipesinc@pipesinc.com',
                                                     sup_phone_number=444555666,
                                                     sup_postal_code='00-220',
                                                     sup_city='Warsaw',
                                                     sup_address='Wiejska 12')
        self.pr1 = Product.objects.create(pr_name='316 SS',
                                          pr_cat='PI',
                                          pr_price=1499.99,
                                          pr_sup=self.test_supplier,
                                          )
        self.url = reverse('product-detail', kwargs={'pk': self.pr1.pr_id})
        self.user_employee = User.objects.create_user(username='empnewbie',
                                                      password='testpass1')
        self.group_employee = Group.objects.create(name='employee')
        self.user_employee.save()
        self.user_employee.groups.add(self.group_employee)

    def test_product_detail_retrieve(self):
        response = self.client.get(self.url)
        get_pr1 = Product.objects.get(pk=self.pr1.pr_id)
        serializer = ProductSerializer(get_pr1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_update(self):
        self.client.login(username='empnewbie', password='testpass1')
        self.data = ProductSerializer(self.pr1).data
        self.data.update({'pr_price': 1299.99})
        response = self.client.put(reverse('product-detail', args=[self.pr1.pr_id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_delete(self):
        self.client.login(username='empnewbie', password='testpass1')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderListView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_customer1 = User.objects.create_user(username='firstuser',
                                                       password='testpass1')

        self.user_customer2 = User.objects.create_user(username='seconduser',
                                                       password='testpass1')
        self.user_employee = User.objects.create_user(username='empnewbie',
                                                      password='testpass1')
        self.group_employee = Group.objects.create(name='employee')
        self.group_customer = Group.objects.create(name='customer')

        self.user_customer1.save()
        self.user_customer2.save()
        self.user_employee.save()
        self.group_employee.save()
        self.group_customer.save()

        # Sample orders to check[GET] for list
        self.or1 = Order.objects.create(or_username=self.user_customer1)
        self.or2 = Order.objects.create(or_username=self.user_customer1)
        self.or3 = Order.objects.create(or_username=self.user_customer2)
        self.or3 = Order.objects.create(or_username=self.user_employee)

        self.user_customer1.groups.add(self.group_customer)
        self.user_customer2.groups.add(self.group_customer)
        self.user_employee.groups.add(self.group_employee)

        self.url = reverse('order-list')

    def test_order_list_retrieve_customer(self):
        self.client.login(username='firstuser', password='testpass1')
        self.assertTrue(self.client.login(username='firstuser', password='testpass1'))
        response = self.client.get(self.url)
        order = Order.objects.filter(or_username=self.user_customer1)
        serializer = OrderSerializer(order, many=True)
        self.assertEqual(order.count(), 2)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_retrieve_employee(self):
        self.client.login(username='empnewbie', password='testpass1')
        self.assertTrue(self.client.login(username='empnewbie', password='testpass1'))
        response = self.client.get(self.url)
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        self.assertEqual(order.count(), 4)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_create_customer(self):
        self.client.login(username='firstuser', password='testpass1')
        self.assertTrue(self.client.login(username='firstuser', password='testpass1'))
        self.data = {}
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_list_create_employee(self):
        self.client.login(username='empnewbie', password='testpass1')
        self.assertTrue(self.client.login(username='empnewbie', password='testpass1'))
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
        self.user_customer1 = User.objects.create_user(username='firstuser',
                                                       password='testpass1')

        self.user_customer2 = User.objects.create_user(username='seconduser',
                                                       password='testpass1')
        self.user_employee = User.objects.create_user(username='empnewbie',
                                                      password='testpass1')
        self.group_employee = Group.objects.create(name='employee')
        self.group_customer = Group.objects.create(name='customer')

        self.user_customer1.save()
        self.user_customer2.save()
        self.user_employee.save()
        self.group_employee.save()
        self.group_customer.save()

        # Sample orders to manipulate
        self.or1 = Order.objects.create(or_username=self.user_customer1)
        self.or2 = Order.objects.create(or_username=self.user_customer1, or_is_finished=True)
        self.or3 = Order.objects.create(or_username=self.user_customer2)

        self.user_customer1.groups.add(self.group_customer)
        self.user_customer2.groups.add(self.group_customer)
        self.user_employee.groups.add(self.group_employee)

        self.test_supplier = Supplier.objects.create(sup_name="Pipes Weld",
                                                     sup_status='',
                                                     sup_email='pipeweld@pipeweld.com',
                                                     sup_phone_number=222555666,
                                                     sup_postal_code='00-220',
                                                     sup_city='Warsaw',
                                                     sup_address='Wiejska 18'
                                                     )

        self.pr1 = Product.objects.create(pr_name='316 SS',
                                          pr_cat='PI',
                                          pr_price=1000,
                                          pr_sup=self.test_supplier,
                                          )

        self.pr2 = Product.objects.create(pr_name='304 SS',
                                          pr_cat='PI',
                                          pr_price=500,
                                          pr_sup=self.test_supplier,
                                          )

        self.pr3 = Product.objects.create(pr_name='CS',
                                          pr_cat='PI',
                                          pr_price=500,
                                          pr_sup=self.test_supplier,
                                          )

        self.pio1 = ProductsInOrders.objects.create(or_id=Order.objects.get(or_id=1),
                                                    pr_id=Product.objects.get(pr_id=1),
                                                    amount=3)

        self.pio2 = ProductsInOrders.objects.create(or_id=Order.objects.get(or_id=1),
                                                    pr_id=Product.objects.get(pr_id=2),
                                                    amount=13)
        self.pio3 = ProductsInOrders.objects.create(or_id=Order.objects.get(or_id=2),
                                                    pr_id=Product.objects.get(pr_id=2),
                                                    amount=8)

        self.url = reverse('order-detail', kwargs={'pk': self.or1.or_id})
        self.url_another_customer = reverse('order-detail', kwargs={'pk': self.or3.or_id})

    def test_order_detail_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_delete = self.client.delete(self.url)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_detail_retrieve_employee(self):
        self.client.login(username='empnewbie', password='testpass1')
        response = self.client.get(self.url)
        get_or1 = Order.objects.get(pk=self.or1.or_id)
        serializer = OrderSerializer(get_or1)
        # self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_retrieve_customer(self):
        self.client.login(username='firstuser', password='testpass1')
        response = self.client.get(self.url)
        get_or1 = Order.objects.get(pk=self.or1.or_id)
        serializer = OrderSerializer(get_or1)
        # self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_another = self.client.get(self.url_another_customer)
        self.assertEqual(response_another.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_update_employee(self):
        self.client.login(username='empnewbie', password='testpass1')
        self.data = OrderSerializer(self.or1).data
        self.data.update({'or_username': self.user_customer2.id, 'or_is_sent': True})
        response = self.client.put(reverse('order-detail', args=[self.or1.or_id]), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_update_customer_valid(self):
        self.client.login(username='firstuser', password='testpass1')
        response_valid1 = self.client.put(reverse('order-detail', args=[self.or1.or_id]), format='json')
        self.assertEqual(response_valid1.status_code, status.HTTP_200_OK)

    def test_order_detail_update_customer_invalid(self):
        self.client.login(username='firstuser', password='testpass1')
        # Other customer's order
        response_invalid1 = self.client.put(reverse('order-detail', args=[self.or3.or_id]), format='json')
        self.assertEqual(response_invalid1.status_code, status.HTTP_400_BAD_REQUEST)
        # Order marked as finished
        response_invalid2 = self.client.put(reverse('order-detail', args=[self.or2.or_id]), format='json')
        self.assertEqual(response_invalid2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_delete_customer(self):
        self.client.login(username='firstuser', password='testpass1')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(self.url_another_customer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_delete_employee(self):
        self.client.login(username='empnewbie', password='testpass1')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
