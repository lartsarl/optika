from django.urls import path

from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('login', views.login, name="login"),
    path('add_to_cart', views.add_to_cart, name="add_to_cart"),
    path('cart', views.cart, name="cart"),
    path('make_order', views.make_order, name="make_order"),
    path('my_purchases', views.my_purchases, name="my_purchases"),
    path('products/<int:id>', views.products, name='products'),
    path('review/<int:id>', views.review, name='review'),
    path('make_appointment', views.make_appointment, name='make_appointment'),
    path('find_slots', views.find_slots, name='find_slots'),
    path('wish_list', views.wish_list, name='wish_list'),
    path('rating', views.rating, name='rating')

]
