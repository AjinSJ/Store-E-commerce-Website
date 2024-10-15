from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('movies/<int:id>/', views.mittaidetails, name='mittaidetails'),
    path('topbrands/<int:id>/', views.Topbrands, name='topbrands'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('add-to-cart/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<int:movie_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
    path('checkout/<int:movie_id>/', views.checkout_view, name='checkout'),
    path('your/payment/endpoint/', views.process_payment, name='process_payment'),
]
