from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('',views.getroutes),
    path('signup/',views.registeruser),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('task/all/',views.getusertasks),
    path('task/add/',views.addtask),
    path('task/get/',views.gettask),
    path('task/add/',views.edittask),
    path('tasky/delete/',views.deletetask),
    path('tasky/complete/',views.completetask),

]