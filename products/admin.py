from django.contrib import admin

from products.models import Baskets, Product, ProductCategory

# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'stripe_produc_price_id', 'category')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Baskets
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
