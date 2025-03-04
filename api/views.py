from rest_framework import viewsets, filters
from orders.models import Dish, Order
from .serializers import DishSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('table_number', 'status')
