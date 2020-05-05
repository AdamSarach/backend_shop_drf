from django.shortcuts import render
from django.http import HttpResponse
from restapi.models import Supplier, Product
from restapi.serializers import SupplierSerializer, ProductSerializer
from rest_framework import generics


def index(request):
    return HttpResponse("Api page.")



class SupplierList(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer