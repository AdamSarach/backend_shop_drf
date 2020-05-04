from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from restapi.models import Supplier
from restapi.serializers import SupplierSerializer


class TestSupplierListView(APITestCase):

    def setUp(self):
        self.url = reverse('supplier-list')
        self.data_valid = {
            "sup_id": 1999,
            "sup_name": "Pipe Valves",
            "sup_status": "",
            "sup_email": "pipevalves@pipevalves.com",
            "sup_phone_number": 444555666,
            "sup_postal_code": "00-220",
            "sup_city": "Warsaw",
            "sup_address": "Wiejska 12"

        }
        self.data_invalid = {
            "sup_id": 2000,
            "sup_name": "",
            "sup_status": "",
            "sup_email": "pipevalves@pipevalves.com",
            "sup_phone_number": 444555666,
            "sup_postal_code": "00-220",
            "sup_city": "Warsaw",
            "sup_address": "Wiejska 12"

        }
        self.newsupplier = Supplier.objects.create(sup_id=1010,
                                                   sup_name="Pipes Weld",
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
        self.assertEqual(Supplier.objects.get(sup_id=1999).sup_name, 'Pipe Valves')

    def test_supplier_list_retrieve(self):
        response = self.client.get(self.url)
        suppliers = Supplier.objects.all()
        print(suppliers)
        serializer = SupplierSerializer(suppliers, many=True)
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSupplierDetailView(APITestCase):

    def setUp(self):
        self.sup1 = Supplier.objects.create(sup_id=1101,
                                            sup_name="Valves inc",
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

    def test_can_delete_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
