from rest_framework import serializers
from restapi.models import Supplier, Product, Order


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['sup_id', 'sup_name', 'sup_status', 'sup_email', 'sup_phone_number', 'sup_postal_code', 'sup_city',
                  'sup_address']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pr_id', 'pr_name', 'pr_cat', 'pr_price', 'pr_sup']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['or_id', 'or_start_date', 'or_is_finished', 'or_finish_date', 'or_is_sent', 'or_sent_date',
                  'or_username']
