import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return 'Категория: ' + self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images')
    description = models.TextField()
    short_description = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stripe_produc_price_id = models.CharField(max_length=128, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'Название: {self.name}, категория: {self.category.name}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_produc_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_produc_price_id = stripe_product_price['id']
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)


    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price*100),
            currency='rub',
        )
        return stripe_product_price


class BuscetQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_produc_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Baskets(models.Model):
    quantity = models.PositiveSmallIntegerField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BuscetQuerySet.as_manager()

    def __str__(self):
        return f'Пользователь {self.user.username}| Товар {self.product.name} '

    def sum(self):
        return self.quantity*self.product.price

    def de_json(self):
        basket_items = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_items

    @classmethod
    def create_or_update(cls, product_id, user):
        baskets = Baskets.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Baskets.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created