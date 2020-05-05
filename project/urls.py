from django.contrib import admin
from django.urls import path
from restapi import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', views.index, name='index'),
    path('api/suppliers', views.SupplierList.as_view(), name='supplier-list'),
    path('api/suppliers/<int:pk>', views.SupplierDetail.as_view(), name='supplier-detail'),
    path('api/products', views.ProductList.as_view(), name='product-list'),
    path('api/products/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
