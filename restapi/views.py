from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404
from django.utils import timezone

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


class OrderList(APIView):
    permission_classes = ((IsAuthenticated & (IsCustomerGroup | IsEmployeeGroup)),)

    def get(self, request, format=None):
        if request.user.groups.filter(name='customer'):
            orders = Order.objects.filter(or_username=request.user)
        elif request.user.groups.filter(name='employee'):
            orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.groups.filter(name='customer'):
            content = {"or_username": request.user.id}
            serializer = OrderSerializer(data=content)
        elif request.user.groups.filter(name='employee'):
            serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

class OrderDetail(APIView):
    permission_classes = ((IsAuthenticated & (IsCustomerGroup | IsEmployeeGroup)),)

    def order_wrong(self):
        return {'message': 'You cannot access an order which isnt yours.'}

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if request.user.groups.filter(name='customer'):
            order = self.get_object(pk)
            if not request.user == order.or_username:
                return Response(self.order_wrong(), status=status.HTTP_400_BAD_REQUEST)
        elif request.user.groups.filter(name='employee'):
            order = self.get_object(pk)

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Customer can only change 'is order finish' status from false to true.
        Employee can change all fields.
        """
        if request.user.groups.filter(name='customer'):
            order = self.get_object(pk)
            if not request.user == order.or_username:
                return Response(self.order_wrong(), status=status.HTTP_400_BAD_REQUEST)
            if not order.or_is_finished:
                data = {'or_is_finished': True, 'or_finish_date': timezone.now()}
                serializer = OrderSerializer(order, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            else:
                order_finished = {'message': 'Your order is already marked as finish. You cannot make any changes.'}
                return Response(order_finished, status=status.HTTP_400_BAD_REQUEST)

        elif request.user.groups.filter(name='employee'):
            order = self.get_object(pk)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if request.user.groups.filter(name='customer'):
            order = self.get_object(pk)
            if not request.user == order.or_username:
                return Response(self.order_wrong(), status=status.HTTP_400_BAD_REQUEST)
        elif request.user.groups.filter(name='employee'):
            order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
