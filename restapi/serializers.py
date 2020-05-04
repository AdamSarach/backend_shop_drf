from rest_framework import serializers
from restapi.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['sup_id', 'sup_name', 'sup_status', 'sup_email', 'sup_phone_number', 'sup_postal_code', 'sup_city',
                  'sup_address']
