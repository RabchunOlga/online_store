from rest_framework import fields, serializers

from products.models import Product, ProductCategory, Baskets

class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'category')


class BasketSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Baskets
        fields = ('id', 'quantity', 'product', 'sum', 'total_sum', 'total_quantity', 'created_timestamp',)
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        return Baskets.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Baskets.objects.filter(user_id=obj.user.id).total_quantity()