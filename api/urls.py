from django.urls import path, include
from rest_framework import routers

from api.views import ProductsModelViewSet, BasketModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductsModelViewSet)
router.register(r'baskets', BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
