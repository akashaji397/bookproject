from . import views
from django.urls import path
from .views import user_detail

urlpatterns = [
    path('user_view/',views.user_view,name='user_view'),
    path('user_detail/<int:book_id>/', user_detail, name='user_detail'),
    path('user_search/',views.user_search,name='user_search'),
    path('userbase/',views.userbase,name='userbase'),
    path('usercart/',views.user_cart,name='user_cart'),
    path('useraddtocart/<int:book_id>/',views.add_to_cart,name='add_to_cart'),
    path('increase_quantity/<int:item_id>/',views.increase_quantity,name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/',views.decrease_quantity,name='decrease_quantity'),
    path('remove_cart/<int:item_id>/',views.remove_from_cart,name='remove_cart'),
    path('create_checkout_session/',views.create_checkout_session,name='create_checkout_session'),
    path('success/',views.success,name='success'),
    path('cancel/',views.cancel,name='cancel'),


]
