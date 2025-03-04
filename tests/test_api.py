import pytest
from orders.models import Order, Dish
from django.urls import reverse
from pytest_django.asserts import assertJSONEqual

@pytest.mark.django_db()
def test_create_order(api_client, api_order_data):
    url = reverse('api:order-list')
    response = api_client.post(url, data=api_order_data, format='json')
    assert response.status_code == 201
    order = Order.objects.get(id=1)
    assert order.table_number == api_order_data['table_number']
    assert list(order.items.values_list('id', flat=True)) == list(api_order_data['items'])
    assert order.status == api_order_data['status']

@pytest.mark.django_db()
def test_cant_create_order_without_dishes(api_client, api_order_data):
    url = reverse('api:order-list')
    api_order_data['items'] = []
    response = api_client.post(url, data=api_order_data, format='json')
    assert response.status_code == 400
    assert 'items' in response.json()
    assert response.json()['items'] == ["В заказе должно быть хотя бы одно блюдо."]
    assert Order.objects.count() == 0

@pytest.mark.django_db()
@pytest.mark.parametrize(
    'status', ('waiting', 'ready', 'paid')
)
def test_change_order_status(api_client, order, status):
    url = reverse('api:order-detail', args=(order.id,))
    response = api_client.patch(url, data={'status': status})
    assert response.status_code == 200
    assert response.json()['status'] == status
    assert Order.objects.get(id=order.id).status == status

@pytest.mark.django_db()
def test_delete_order(api_client, order):
    url = reverse('api:order-detail', args=(order.id,))
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Order.objects.count() == 0