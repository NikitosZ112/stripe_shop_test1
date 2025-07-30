from django.db import models

class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'Euro'),
        ('rub', 'RUB'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена в центах", help_text="Например, 1500 = 15.00 USD")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='rub', verbose_name="Валюта")
    image = models.ImageField(upload_to='item_images/', blank=True, null=True, verbose_name="Фото товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def currency_symbol(self):
        return {'usd': '$', 'eur': '€', 'rub': '₽'}.get(self.currency, self.currency.upper())

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']  # Новые товары сверху

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название скидки")
    percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент скидки",
                                  help_text="Процент, например 10.50 для скидки 10,5%")
    description = models.TextField(blank=True, null=True, verbose_name="Описание скидки")

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

class Tax(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название налога")
    percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент налога",
                                  help_text="Процент, например 20.00 для 20% НДС")
    description = models.TextField(blank=True, null=True, verbose_name="Описание налога")

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

class Order(models.Model):
    items = models.ManyToManyField('Item', verbose_name="Товары")  # M2M, чтобы один заказ мог содержать много товаров
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    paid = models.BooleanField(default=False, verbose_name="Оплачен")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name="Скидка")
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL,
                            null=True, blank=True, verbose_name="Налог")
    email = models.EmailField(blank=True, null=True, verbose_name="Email заказчика")
    customer_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="Имя покупателя")
    stripe_order_id = models.CharField(max_length=128, blank=True, null=True, verbose_name="Stripe Order ID")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.pk} ({self.created_at.date()})"

    @property
    def base_sum(self):
        "Общая стоимость товаров без учета скидок и налогов"
        return sum(item.price for item in self.items.all())

    @property
    def discount_amount(self):
        if self.discount:
            return self.base_sum * float(self.discount.percent) / 100
        return 0

    @property
    def tax_amount(self):
        if self.tax:
            return (self.base_sum - self.discount_amount) * float(self.tax.percent) / 100
        return 0

    @property
    def total(self):
        # Итоговая сумма заказа с учетом скидки и налога
        return int(self.base_sum - self.discount_amount + self.tax_amount)