from django.conf.urls import url
from . import views


app_name = 'shop'

urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^user_logout/$',views.user_logout,name='user_logout'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),   
]
    