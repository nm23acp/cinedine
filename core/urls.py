from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_ticket, name='book_ticket'),
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
]