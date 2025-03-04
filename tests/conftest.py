import pytest
from orders.models import Dish, Order
from django.test.client import Client
from rest_framework.test import APIClient

@pytest.fixture
def dish():
    return Dish.objects.create(name='Test dish', price=100)

@pytest.fixture
def order(dish):
    order = Order.objects.create(table_number=1)
    order.items.add(dish)
    return order

@pytest.fixture
def form_data(dish):
    return {
        'table_number': 1,
        'items': (dish.id,)
    }

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def api_order_data(dish):
    return {
        'table_number': 1,
        'status': 'waiting',
        'items': (dish.id,)
    }
