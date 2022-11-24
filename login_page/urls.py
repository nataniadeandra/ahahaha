from django.urls import path
from . import views

app_name = 'login_page'

urlpatterns = [
    path('init/', views.init, name='init'),
    path('login/', views.login, name='login'),
    path('register/home', views.register, name='register'),
    path('register/admin', views.register_admin, name='register_admin'),
    path('register/cust', views.register_cust, name='register_cust'),
    path('register/rest', views.register_rest, name='register_rest'),
    path('register/cour', views.register_cour, name='register_cour')
]