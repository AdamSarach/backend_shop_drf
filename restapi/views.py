from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from restapi.models import Supplier, Product, Order
from restapi.serializers import SupplierSerializer, ProductSerializer, OrderSerializer
from restapi.permissions import IsOrderOwner, IsEmployeeGroup, IsCustomerGroup

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


# class OrderList(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
# #     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class OrderList(APIView):
    def get(self, request, format=None):
        permission_classes = (IsAuthenticated & (IsCustomerGroup | IsEmployeeGroup))
        if IsCustomerGroup:
            orders = Order.objects.filter(or_username=request.user)
        elif IsEmployeeGroup:
            orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        permission_classes = (IsAuthenticated & (IsCustomerGroup | IsEmployeeGroup))
        if IsCustomerGroup:
            content = {"or_username": request.user.id}
            serializer = OrderSerializer(data=content)
        elif IsEmployeeGroup:
            serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
