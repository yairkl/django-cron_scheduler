from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:day>/', views.day, name='day'),
    path('setState/<int:id>/<int:state>',views.setState,name='setState'),
    path('getState/<int:id>',views.getState,name='getState'),
]

