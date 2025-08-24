from django.urls import path
from . import views

urlpatterns = [
    path('',views.getroutes),
    path('getalltasks/',views.getalltasks),
    path('getusertasks/<str:pk>',views.getusertasks),
    path('getcurrentusertasks/',views.getcurrentusertasks),
    path('SignUp/',views.registeruser),
    path('login/',views.loginuser),
]