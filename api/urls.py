from rest_framework import routers
from .views import OrderViewSet, DishViewSet
from django.urls import path, include

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'dishes', DishViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]
