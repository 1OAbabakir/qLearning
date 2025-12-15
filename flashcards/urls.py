from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('study/<str:category>/', views.study, name='study'),
    path('add/', views.add_card, name='add_card'),
    path('card/<int:card_id>/image/', views.card_image, name='card_image'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
