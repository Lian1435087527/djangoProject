from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [path('', handle_wx), path('create_menu/', create_menu)]
