from django.conf.urls import url
from . import views
from django.urls import path
from .views import PaymentView, GeneratePDF, RequestRefundView

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'), 
    path('charge/', views.charge, name='charge'), 
    path('cash/',views.cash, name='cash'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    url(r'^invoice/$', GeneratePDF.as_view(), name='invoice'),
    path('refund/', RequestRefundView.as_view(), name='refund')

]