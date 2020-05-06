from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from restapi.models import Supplier, Product, Order, User
from restapi.serializers import SupplierSerializer, ProductSerializer, OrderSerializer


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

    def test_product_list_create(self):
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

    def test_product_detail_retrieve(self):
        response = self.client.get(self.url)
        get_pr1 = Product.objects.get(pk=self.pr1.pr_id)
        serializer = ProductSerializer(get_pr1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_update(self):
        self.data = ProductSerializer(self.pr1).data
        self.data.update({'pr_price': 1299.99})
        response = self.client.put(reverse('product-detail', args=[self.pr1.pr_id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderListView(APITestCase):

    def setUp(self):
        self.url = reverse('order-list')
        self.test_user = User.objects.create(username='firstuser',
                                             password='testpass1')
        self.valid_user = User.objects.get(username='firstuser')
        self.data_valid = {"or_username": self.valid_user.id}

    def test_order_list_create(self):
        response_valid = self.client.post(self.url, self.data_valid, format='json')
        self.assertEqual(response_valid.status_code, status.HTTP_201_CREATED)


class TestOrderDetailView(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='firstuser',
                                             password='testpass1')
        self.test_user2 = User.objects.create(username='seconduser',
                                              password='testpass1')
        self.or1 = Order.objects.create(or_username=self.test_user)
        self.url = reverse('order-detail', kwargs={'pk': self.or1.or_id})

    def test_order_detail_retrieve(self):
        response = self.client.get(self.url)
        get_pr1 = Order.objects.get(pk=self.or1.or_id)
        serializer = OrderSerializer(get_pr1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_update(self):
        self.data = OrderSerializer(self.or1).data
        self.data.update({'or_username': self.test_user2.id})
        response = self.client.put(reverse('order-detail', args=[self.or1.or_id]), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
