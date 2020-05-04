from django.shortcuts import render
from django.http import HttpResponse
from restapi.models import Supplier
from restapi.serializers import SupplierSerializer
from rest_framework import generics


def index(request):
    return HttpResponse("Api page.")


class SupplierList(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
