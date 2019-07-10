from django.contrib import admin
from .models import Order, OrderItem, Payment, Refund


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',  'city', 'created','received', 'refund_request', 'refund_granted']
    list_filter = [ 'created', 'updated','received', 'refund_request', 'refund_granted']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem)
