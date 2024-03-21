from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from products.serializers import ProductsSerializer, BasketSerializer
from products.models import Product, Baskets

class ProductsModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class BasketModelViewSet(ModelViewSet):
    queryset = Baskets.objects.all()
    serializer_class = BasketSerializer
    # permission_classes = (IsAuthenticated,)
    pagination_class = None

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'No product with such ID.'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Baskets.create_or_update(products.first().id, self.request.user)
            serializer = self.get_serializer(obj)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product_id': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)