from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:day>/', views.day, name='day'),
    path('setState/<int:id>/<int:state>',views.set_state,name='setState'),
    path('getState/<int:id>',views.get_state,name='getState'),
]

