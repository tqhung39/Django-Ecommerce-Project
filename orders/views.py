from django.shortcuts import render, redirect,  get_object_or_404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import OrderItem, Order, Refund
from .forms import OrderCreateForm, RefundForm
from django.views.generic.base import TemplateView
from cart.cart import Cart
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .utils import render_to_pdf
from django.contrib import messages
import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_refund_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, 'orders/refund.html', context)
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            refund_code = form.cleaned_data.get('refund_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(refund_code = refund_code)
                order.refund_requested = True
                order.save()
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                message.info(self.request, "Your request has been received.")
                return redirect("orders:refund")
            except ObjectDoesNotExist:
                message.info(self.request, "This order is not exist.")
                return redirect("orders:refund")

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    discount_price=item['discount_price'],
                    quantity=item['quantity']
                )
            cart.clear()
        return redirect('orders:payment')
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/checkout.html',{'form': form})

def cash(request):
    cart = Cart(request)
    order = Order(request.POST or None)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    discount_price=item['discount_price'],
                    quantity=item['quantity']
                )
            cart.clear()
        return redirect('orders:invoice')
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/checkout.html',{'form': form})

class PaymentView(TemplateView):
    template_name = 'orders/payment.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request): 
    order = Order(request.POST or None)
    if request.method == 'POST':
            charge = stripe.Charge.create(
            amount=9999,
            currency='usd',
            source=request.POST['stripeToken']
        
        )
    return redirect('orders:invoice')



class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        orderitem = OrderItem.objects.all()
        order = Order.objects.all()
        id = order[0].id
        first_name = order[0].first_name
        last_name = order[0].last_name
        email = order[0].email
        address = order[0].address
        city = order[0].city
        country = order[0].country
        payment = order[0].payment
        amount = order[0].get_total_cost
        today = order[0].created
        item = orderitem[0].product 
        quantity = orderitem[0].quantity 
        template = get_template('invoice.html')
        context = {
            "invoice_id": id,
            'first_name': first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "city": city,
            "country": country,
            "payment": payment,
            "item": item,
            "quantity": quantity,
            "amount": amount,
            "today": today,
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
