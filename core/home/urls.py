from django.urls import path,include
from home.views import *

urlpatterns = [
    path('',home,name="home"),
    path('logout/',logout_request,name="logout_request"),
    path('ask/',chat,name="chat"),
]
