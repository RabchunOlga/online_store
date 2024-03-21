from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration_time')
    fields = ('code', 'user', 'expiration_time', 'create_date')
    readonly_fields = ('create_date',)
