from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # 👈 this line
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('thankyou/', views.thank_you_view, name='thankyou'),
    path('ajax/add-to-cart/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('ajax/update-cart/', views.ajax_update_cart, name='ajax_update_cart'),
    path('ajax/remove-from-cart/', views.ajax_remove_from_cart, name='ajax_remove_from_cart'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

]
