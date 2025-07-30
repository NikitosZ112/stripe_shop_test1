from django.contrib import admin
from .models import Item, Order, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'description')
    search_fields = ('name',)

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'description')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'email', 'paid', 'created_at', 'discount', 'tax', 'total_amount')
    list_filter = ('paid', 'created_at', 'discount', 'tax')
    search_fields = ('customer_name', 'email', 'stripe_order_id')

    filter_horizontal = ('items',)

    def total_amount(self, obj):
        # Вывод итоговой суммы заказа с учетом скидок и налогов
        return obj.total  # предполагается, что в модели есть свойство total
    total_amount.short_description = "Итоговая сумма"

