from django.urls import path
from . import views

app_name='topfragmarket'

urlpatterns = [
   path('', views.index, name='home'),
   path('categories/', views.categories, name='categories'), 
   path('login/', views.login, name='login'), 
]