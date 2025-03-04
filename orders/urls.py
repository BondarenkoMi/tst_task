from django.urls import path
from .views import OrderCreateView, OrderListView, DishCreateView, get_revenue, delete_order, update_order_status

app_name = 'orders'

urlpatterns = [
    path('revenue', get_revenue, name='revenue'),
    path('create', OrderCreateView.as_view(), name='create'),
    path('create_dish', DishCreateView.as_view(), name='create_dish'),
    path('<int:pk>/update_status', update_order_status, name='update_status'),
    path('<int:pk>/delete', delete_order, name='delete'),
    path('', OrderListView.as_view(), name='list')
]
