from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Baskets, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store_'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = '_Store - Каталог'
    category = 0

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        self.category = category_id if category_id else 0
        if category_id:
            category_id = self.category
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # cache
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories

        # context['categories'] = ProductCategory.objects.all()

        context['category_id'] = self.category
        return context


@login_required
def baskets_add(request, product_id):
    Baskets.create_or_update(product_id, request.user)
    # product = Product.objects.get(id=product_id)
    # baskets = Baskets.objects.filter(user=request.user, product=product)
    # if not baskets.exists():
    #     Baskets.objects.create(user=request.user, product=product, quantity=1)
    # else:
    #     basket = baskets.first()
    #     basket.quantity += 1
    #     basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def baskets_remove(request, basket_id):
    basket = Baskets.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# def index(request):
#     context = {
#         'title': 'Store_',
#         'is_promo': False
#     }
#     return render(request, 'products/index.html', context)

# def products(request, category_id=None, page_number=1):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     product_paginator = paginator.page(page_number)
#     context = {
#         'title': '_Store - Каталог',
#         'products' : product_paginator,
#         'categories' : ProductCategory.objects.all()
#      }
#     return render(request, 'products/products.html', context)

