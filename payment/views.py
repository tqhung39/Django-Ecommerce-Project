from django.shortcuts import render, redirect,  get_object_or_404
from django.conf import settings
from django.urls import reverse
from cart.cart import Cart
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

def process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html')

@csrf_exempt
def done(request):
    return render(request, 'payment/done.html')
 
 
@csrf_exempt
def canceled(request):
    return render(request, 'payment/cancelled.html')