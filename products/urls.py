from django.urls import path

from products.views import ProductsListView, baskets_add, baskets_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>', ProductsListView.as_view(), name='category'),
    #path('page/<int:page>', ProductsListView.as_view(), name='paginator'),
    path('page/<int:page>/<int:category_id>', ProductsListView.as_view(), name='paginator'),
    # #path('category/<int:category_id>/page/<int:page_number>', products, name='paginator'),
    path('baskets/add/<int:product_id>', baskets_add, name='baskets_add'),
    path('baskets/remove/<int:basket_id>', baskets_remove, name='baskets_remove'),
]
