from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'payment'

urlpatterns = [
    path('process-payment/', views.process, name='process'),
    path('payment-done/', views.done, name='done'),
    path('payment-cancelled/', views.canceled, name='cancelled'),
]