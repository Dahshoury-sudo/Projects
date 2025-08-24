from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('add-task/',views.addtask,name='add'),
    path('task/<str:pk>',views.showtask,name = 'task'),
    path('delete-task/<str:pk>',views.deletetask,name='delete-task')
]