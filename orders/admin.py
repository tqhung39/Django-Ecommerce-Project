from django.contrib import admin
from .models import Order, OrderItem, Payment, Refund

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_request=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',  'city', 'created','received', 'refund_request', 'refund_granted']
    list_filter = [ 'created', 'updated','received', 'refund_request', 'refund_granted']
    inlines = [OrderItemInline]
    search_fields = ['refund_code']
    actions = [make_refund_accepted]

admin.site.register(Order, OrderAdmin)
admin.site.register(Refund)
admin.site.register(OrderItem)
