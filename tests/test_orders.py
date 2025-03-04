import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError
from orders.models import Order, Dish
from orders.forms import OrderForm


@pytest.mark.django_db()
def test_create_order(form_data, client):
    url = reverse('orders:create')
    response = client.post(url, data=form_data)
    assertRedirects(response, reverse('orders:list'))
    order = Order.objects.get(id=1)
    assert Dish.objects.count() == 1
    assert Order.objects.count() == 1
    assert order.items.count() == 1
    assert order.table_number == form_data['table_number']
    assert order.items.get().id == form_data['items'][0]

@pytest.mark.django_db()
def test_cant_create_order_without_dishes(client):
    url = reverse('orders:create')
    form_data = {
        'table_number': 1,
        'items': []
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assert 'form' in response.context
    form = response.context['form']
    assert isinstance(form, OrderForm)
    assertFormError(form, 'items', 'В заказе должно быть хотябы 1 блюдо.')
    assert Order.objects.count() == 0

@pytest.mark.django_db()
def test_change_order_status(order):
    assert order.status == 'waiting'
    order.status = 'ready'
    assert order.status == 'ready'
    order.status = 'paid'
    assert order.status == 'paid'

@pytest.mark.django_db()
def test_delete_order(order, client):
    assert Order.objects.count() == 1
    delete_url = reverse('orders:delete', args=(order.id,))
    response = client.get(delete_url)
    assertRedirects(response, reverse('orders:list'))
    assert Order.objects.count() == 0

@pytest.mark.django_db()
def test_get_revenue(order, client):
    revenue_url = reverse('orders:revenue')
    response = client.get(revenue_url)
    assert response.status_code == 200
    assert 'revenue' in response.context
    revenue = response.context['revenue']
    assert revenue == 0
    order.status = 'paid'
    order.save()
    exp_revenue = order.total_price
    response = client.get(revenue_url)
    assert response.status_code == 200
    assert 'revenue' in response.context
    revenue = response.context['revenue']
    assert revenue == exp_revenue