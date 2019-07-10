from django.db import models
from shop.models import Product
from django.conf import settings
from django_countries.fields import CountryField
PAYMENT_CHOICES = (
    ('Stripe', 'Stripe'),
    ('PayPal', 'PayPal')
)
class Order(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    refund_code = models.CharField(max_length=200)
    paid = models.BooleanField(default=False)
    payment = models.CharField(max_length=10,choices=PAYMENT_CHOICES, default='Stripe')
    country = CountryField()
    received = models.BooleanField(default=False)
    refund_request = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('order',)
    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return (self.price - self.discount_price) * self.quantity 

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    def __str__(self):
        return f"{self.pk}"

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

