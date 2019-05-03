from django.urls import re_path
from . import views

app_name = 'request'

urlpatterns = [
    re_path(r'^create/$', views.create_order, name='create_order'),
]
